"""邮箱下载工具

功能:
- 支持多邮箱服务商(QQ, Gmail, 163, Outlook等)
- 图形化界面操作
- 下载邮件正文(纯文本/HTML)
- 下载邮件附件
- 多线程并发下载
- 断点续传支持
- 下载进度显示
- 记住账号密码功能

作者: Himalaya
版本: 1.1.0
"""

from email.message import Message
import email.header
import imaplib
import sys
import os
import re
import json
import time
import logging
import threading
from typing import Optional, Tuple, Dict, List, Union, Callable, Any, Generator
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from email.parser import BytesParser
from email.utils import parsedate_to_datetime, parseaddr
from email.header import make_header, decode_header
from pathlib import Path
from threading import Thread, Lock
from dataclasses import dataclass

import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QObject, QThread, Qt, pyqtSignal
import ui_EmailDownload

# 配置日志
def setup_logging():
    """配置日志记录"""
    try:
        # 确保日志目录存在且有写入权限
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # 检查日志文件权限
        log_file = log_dir / 'email_downloader.log'
        if log_file.exists():
            try:
                with open(log_file, 'a') as f:
                    f.write('')
            except PermissionError:
                print(f"无权限写入日志文件: {log_file}")
                return
        
        # 配置日志
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # 清除已有handler
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            
        # 文件handler
        file_handler = logging.FileHandler(
            str(log_file),
            encoding='utf-8',
            mode='a'  # 追加模式
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        
        # 控制台handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
    except Exception as e:
        logger.error(f"日志配置失败: {e}")
        raise
    finally:
        logger.info("日志配置完成")

    # 捕获未处理异常
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logger.critical("未捕获异常", 
            exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = handle_exception

setup_logging()
logger = logging.getLogger(__name__)

def main():
    """主程序入口"""
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    
    # 加载UI文件
    window = QMainWindow()
    ui = ui_EmailDownload.Ui_MainWindow()
    ui.setupUi(window)
    
    # 设置窗口标题、样式和背景
    window.setWindowTitle('Email Download Tool -- By Himalaya')
    window.setStyleSheet(open('styles.qss', encoding='utf-8').read())
    
    # 添加背景图片
    if os.path.exists('background.png'):
        background = QLabel(window)
        pixmap = QPixmap('background.png')
        background.setPixmap(pixmap)
        background.setScaledContents(True)
        background.setGeometry(0, 0, window.width(), window.height())
        background.lower()  # 将背景置于底层
    
    # 连接信号槽 - 修复后的版本
    def handle_start_download():
        ui.start_download()
    ui.confirm.clicked.connect(handle_start_download)
    
    # 主题切换功能 - 修复后的版本
    def handle_toggle_theme():
        ui.toggle_theme()
    ui.themeButton.clicked.connect(handle_toggle_theme)
    
    # 加载保存的凭证和主题
    ui.load_credentials()
    ui.load_theme = ui.toggle_theme  # 将主题切换函数赋值给load_theme
    
    # 显示窗口
    window.show()
    sys.exit(app.exec_())

# 修复后的记住密码功能
def save_credentials(ui):
    """保存邮箱、密码和主题到credentials.json"""
    try:
        # 检查cryptography模块是否安装
        try:
            import cryptography
            from cryptography.fernet import Fernet
            crypto_available = True
        except ImportError:
            crypto_available = False
            logger.warning("cryptography模块未安装，密码将以明文存储")

        data = {}
        if os.path.exists('credentials.json'):
            with open('credentials.json', 'r') as f:
                data = json.load(f)
        
        # 保存邮箱
        if ui.checkBox.isChecked():
            data['email'] = ui.mailAddress.text()
            data['email_address_check'] = True
            logger.info("保存邮箱地址")
        else:
            data.pop('email', None)
            data['email_address_check'] = False
            logger.info("不保存邮箱地址")
            
        # 保存密码
        if ui.checkBox_2.isChecked():
            # 加密密码
            if crypto_available:
                try:
                    key = Fernet.generate_key()
                    cipher_suite = Fernet(key)
                    encrypted_pwd = cipher_suite.encrypt(ui.imapPassword.text().encode())
                    data['password'] = f"enc:{encrypted_pwd.decode()}"
                    data['password_key'] = key.decode()
                    data['password_check'] = True
                    logger.info("保存加密密码")
                except Exception as e:
                    logger.error(f"密码加密失败: {e}")
                    data['password'] = ui.imapPassword.text()
                    data['password_check'] = True
                    logger.info("保存未加密密码")
            else:
                data['password'] = ui.imapPassword.text()
                data['password_check'] = True
                logger.info("cryptography模块不可用，保存未加密密码")
        else:
            data.pop('password', None)
            data.pop('password_key', None)
            data['password_check'] = False
            logger.info("不保存密码")
        
        # 保存主题
        data['theme'] = ui.themeButton.property('theme')
        
        with open('credentials.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"保存凭据失败: {e}")
        QMessageBox.warning(None, "错误", f"保存凭据失败: {e}")

if __name__ == "__main__":
    main()
