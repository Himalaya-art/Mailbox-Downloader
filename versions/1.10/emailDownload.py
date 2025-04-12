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

import email
import email.header
import email.message
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
from email.utils import parsedate_to_datetime , parseaddr
from email.header import make_header, decode_header
from pathlib import Path
from threading import Lock , Thread
from dataclasses import dataclass

import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSignal , Qt
import ui_EmailDownload

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_downloader.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DownloadStats:
    total: int = 0
    success: int = 0
    failed: int = 0
    attachments: int = 0

class Tools:
    """邮件处理工具类"""
    
    @staticmethod
    def rename(email_id: bytes, msg: email.message.Message, base_path: str) -> str:
        """重命名邮件文件路径，包含时间戳和邮件ID
        
        Args:
            email_id: 邮件ID
            msg: 邮件消息对象
            base_path: 基础路径
            
        Returns:
            str: 格式化后的路径字符串
            
        Raises:
            Exception: 如果日期解析失败
        """
        try:
            if msg['Date']:
                email_time = parsedate_to_datetime(msg['Date']).strftime('%Y-%m-%d %H-%M-%S')
                return f"{base_path}_{email_time}_{email_id.decode('utf-8')}"
            return f"{base_path}_{email_id.decode('utf-8')}"
        except Exception as e:
            logger.error(f"重命名邮件失败: {e}")
            return f"{base_path}_{int(time.time())}_{email_id.decode('utf-8')}"

class ProgressSignal(QObject):
    """
    进度信号类，用于在下载过程中发送进度更新信号
    """
    """进度信号类
    
    Signals:
        progress (int): 下载进度百分比
        stats_updated (dict): 下载统计信息更新
        error_occurred (str): 错误发生时发送信号
    """
    progress = pyqtSignal(int)
    stats_updated = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

class EmailDownload:
    """邮件下载核心类
    
    Attributes:
        MAX_RETRIES (int): 最大重试次数
        RETRY_DELAY (int): 重试延迟(秒)
        MAX_WORKERS (int): 最大线程数
        CHUNK_SIZE (int): 文件分块大小(字节)
    """
    
    MAX_RETRIES = 3
    RETRY_DELAY = 2
    MAX_WORKERS = 4
    CHUNK_SIZE = 1024 * 1024  # 1MB
    
    @staticmethod
    @contextmanager
    def imap_connection(email_address: str, password: str) -> Generator[imaplib.IMAP4_SSL, None, None]:
        """IMAP连接上下文管理器
        
        Args:
            email_address: 邮箱地址
            password: 邮箱密码
            
        Yields:
            IMAP4_SSL: IMAP连接对象
            
        Raises:
            Exception: 连接或登录失败时抛出异常
        """
        mail = None
        try:
            domain = email_address.split("@")[1]
            mail_server = EmailDownload.get_imap_server(domain)
            mail = imaplib.IMAP4_SSL(mail_server, timeout=30)
            mail.login(email_address, password)
            yield mail
        except Exception as e:
            logger.error(f"IMAP连接错误: {e}")
            raise
        finally:
            if mail:
                try:
                    mail.close()
                    mail.logout()
                except Exception as e:
                    logger.warning(f"关闭IMAP连接时出错: {e}")

    @staticmethod
    def get_imap_server(domain: str) -> str:
        """获取IMAP服务器地址
        
        Args:
            domain: 邮箱域名(如qq.com)
            
        Returns:
            IMAP服务器地址
            
        Note:
            优先从imap_servers.json读取配置，失败则使用内置默认值
        """
        try:
            with open('imap_servers.json', 'r') as f:
                config = json.load(f)
                return config['servers'].get(domain, f"imap.{domain}")
        except Exception as e:
            logger.warning(f"读取IMAP服务器配置失败，使用默认值: {e}")
            default_servers = {
                "qq.com": "imap.qq.com",
                "gmail.com": "imap.gmail.com", 
                "163.com": "imap.163.com",
                "outlook.com": "imap-mail.outlook.com"
            }
            return default_servers.get(domain, f"imap.{domain}")

    @staticmethod
    def download_emails(
        email_address: str, 
        password: str, 
        ui: Any,
        progress_signal: ProgressSignal
    ) -> Optional[DownloadStats]:
        """下载所有未读邮件
        
        Args:
            email_address: 邮箱地址
            password: 邮箱密码
            ui: 用户界面对象
            progress_signal: 进度信号对象
            
        Returns:
            DownloadStats: 下载统计信息
        """
        try:
            with EmailDownload.imap_connection(email_address, password) as mail:
                mail.select("INBOX")
                status, email_ids = mail.search(None, 'UNSEEN')
                if status != 'OK' or not email_ids or not email_ids[0]:
                    ui.changeTitle('Email Download Tool | 没有未读邮件 -- By Himalaya')
                    progress_signal.stats_updated.emit({
                        'total': 0,
                        'downloaded': 0,
                        'failed': 0
                    })
                    return None
                
                # 确保email_ids[0]是bytes或str类型
                if isinstance(email_ids[0], (bytes, str)):
                    email_list = email_ids[0].split() if isinstance(email_ids[0], bytes) else email_ids[0].encode().split()
                else:
                    logger.error(f"无效的邮件ID格式: {type(email_ids[0])}")
                    raise ValueError("无效的邮件ID格式")
                
                if not email_list:
                    ui.changeTitle('Email Download Tool | 没有未读邮件 -- By Himalaya')
                    progress_signal.stats_updated.emit({
                        'total': 0,
                        'downloaded': 0,
                        'failed': 0
                    })
                    return None

                # 检查是否有上次未完成的下载
                stats = DownloadStats(total=len(email_list))
                if ui.resumeDownload.isChecked():
                    resume_data = EmailDownload._check_resume_data(email_address)
                    if resume_data:
                        email_list = [eid for eid in email_list if eid not in resume_data['completed']]
                        stats = DownloadStats(
                            total=len(email_list) + len(resume_data['completed']),
                            success=len(resume_data['completed']),
                            failed=resume_data['failed']
                        )
                lock = Lock()
                
                def update_progress(success: bool = True, email_id: Optional[bytes] = None):
                    """更新进度和统计信息
                    
                    Args:
                        success: 是否成功下载
                        email_id: 邮件ID(用于断点续传)
                    """
                    with lock:
                        if success:
                            stats.success += 1
                            if email_id:
                                EmailDownload._update_resume_data(email_address, email_id, success=True)
                        else:
                            stats.failed += 1
                            if email_id:
                                EmailDownload._update_resume_data(email_address, email_id, success=False)
                        
                        progress = int((stats.success + stats.failed) / stats.total * 100)
                        progress_signal.progress.emit(progress)
                        progress_signal.stats_updated.emit({
                            'total': stats.total,
                            'downloaded': stats.success,
                            'failed': stats.failed,
                            'resume': len(email_list)  # 可续传的邮件数量
                        })

                # 使用线程池并行下载邮件
                with ThreadPoolExecutor(max_workers=EmailDownload.MAX_WORKERS) as executor:
                    futures = {
                        executor.submit(
                            EmailDownload.download_email,
                            email_id, email_address, password, ui, update_progress
                        ): email_id for email_id in email_list
                    }
                    
                    # 等待所有任务完成并处理结果
                    for future in as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                            logger.error(f"邮件下载失败: {e}")
                            update_progress(False)

                ui.changeTitle('Email Download Tool | 下载完成! -- By Himalaya')
                logger.info(f"成功下载 {len(email_list)} 封邮件")

                # 如果勾选了"下载后标记为已读"
                if ui.seenAfterDownload.isChecked():
                    try:
                        mail.select("INBOX")
                        for email_id in email_list:
                            mail.store(email_id, '+FLAGS', '\\Seen')
                        logger.info(f"成功标记 {len(email_list)} 封邮件为已读")
                    except Exception as e:
                        logger.error(f"标记邮件为已读失败: {e}")

        except Exception as e:
            logger.error(f"下载邮件失败: {e}")
            ui.changeTitle('Email Download Tool | 错误 -- By Himalaya')
    
    @staticmethod
    def download_email(
        email_id: bytes, 
        email_address: str, 
        password: str, 
        ui: Any, 
        progress_callback: Optional[Callable[[bool], None]] = None
    ) -> None:
        """下载单个邮件
        
        Args:
            email_id: 邮件ID
            email_address: 邮箱地址
            password: 邮箱密码
            ui: 用户界面对象
            progress_callback: 进度回调函数
            
        Raises:
            Exception: 下载失败时抛出异常
        """
        msg = None
        
        for attempt in range(EmailDownload.MAX_RETRIES):
            try:
                with EmailDownload.imap_connection(email_address, password) as mail:
                    mail.select("INBOX")
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    if status != 'OK' or not msg_data or not msg_data[0]:
                        raise Exception(f"获取邮件失败: {status}")
                
                # 确保msg_data是预期格式
                if isinstance(msg_data[0], tuple) and len(msg_data[0]) >= 2:
                    msg_content = msg_data[0][1]
                    if isinstance(msg_content, (bytes, str)):
                        msg = BytesParser().parsebytes(msg_content if isinstance(msg_content, bytes) else msg_content.encode())
                    else:
                        raise Exception("无效的邮件内容格式")
                else:
                    raise Exception("无效的邮件数据结构")
                break
            except (imaplib.IMAP4.abort, ConnectionError) as e:
                if attempt < EmailDownload.MAX_RETRIES - 1:
                    time.sleep(EmailDownload.RETRY_DELAY)
                    continue
                logger.error(f"下载邮件失败(尝试 {EmailDownload.MAX_RETRIES} 次): {e}")
                if progress_callback:
                    progress_callback(False)
                raise
            except Exception as e:
                logger.error(f"下载邮件时发生错误: {e}")
                if progress_callback:
                    progress_callback(False)
                raise

        subject = make_header(decode_header(msg['SUBJECT']))
        subject = re.sub(r'[\\/:*?"<>|]', '', str(subject)).strip()
        valid_subject = f'无主题_{int(time.time())}' if not subject or subject.isspace() else subject
        
        # 创建下载目录
        download_dir = Path(f'./downloads/{email_address}')
        path = Tools.rename(email_id, msg, str(download_dir / valid_subject))
        Path(path).mkdir(parents=True, exist_ok=True)

        # 处理邮件内容
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    EmailDownload._process_email_part(part, path, valid_subject, ui)
            else:
                EmailDownload._save_text_content(msg, path, valid_subject)

            # 处理附件
            attachment_count = 0
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart' or part.get("Content-Disposition") is None:
                    continue
                if EmailDownload._save_attachment(part, path, ui):
                    attachment_count += 1

            if progress_callback:
                progress_callback(True)

            return attachment_count
        except Exception as e:
            logger.error(f"处理邮件内容失败: {e}")
            if progress_callback:
                progress_callback(False)
            raise

    @staticmethod
    def _process_email_part(
        part: email.message.Message, 
        path: str, 
        valid_subject: str, 
        ui: Any
    ) -> None:
        """处理邮件各部分内容
        
        Args:
            part: 邮件部分对象
            path: 保存路径
            valid_subject: 有效主题
            ui: 用户界面对象
            
        Note:
            根据内容类型调用相应的保存方法
        """
        content_type = part.get_content_type()
        charset = part.get_content_charset() or 'utf-8'

        try:
            if content_type == 'text/plain':
                EmailDownload._save_text_file(part, path, valid_subject, charset)
            elif content_type == 'text/html' and ui.downloadHTML.isChecked():
                EmailDownload._save_html_file(part, path, valid_subject, charset)
            elif 'image' in content_type:
                EmailDownload._save_image_file(part, path, valid_subject)

        except Exception as e:
            logger.warning(f"处理邮件部分内容失败: {e}")

    @staticmethod
    def _save_text_file(
        part: email.message.Message, 
        path: str, 
        valid_subject: str, 
        charset: str
    ) -> None:
        """保存纯文本内容
        
        Args:
            part: 邮件部分对象
            path: 保存路径
            valid_subject: 有效主题
            charset: 字符编码
        """
        txt_filepath = os.path.join(path, f'{valid_subject}.txt')
        content = part.get_payload(decode=True).decode(charset)
        with open(txt_filepath, 'w', encoding='UTF-8') as f:
            f.write(content)

    @staticmethod
    def _save_html_file(
        part: email.message.Message, 
        path: str,
        valid_subject: str, 
        charset: str
    ) -> None:
        """保存HTML内容
        
        Args:
            part: 邮件部分对象
            path: 保存路径
            valid_subject: 有效主题
            charset: 字符编码
        """
        html_filepath = os.path.join(path, f'{valid_subject}.html')
        content = part.get_payload(decode=True).decode(charset)
        with open(html_filepath, 'w', encoding='UTF-8') as f:
            f.write(content)

    @staticmethod
    def _save_image_file(
        part: email.message.Message, 
        path: str,
        valid_subject: str
    ) -> None:
        """保存图片内容
        
        Args:
            part: 邮件部分对象
            path: 保存路径
            valid_subject: 有效主题
        """
        content_type = part.get_content_type()
        ext = content_type.split('/')[1]
        image_filepath = os.path.join(path, f'{valid_subject}.{ext}')
        with open(image_filepath, 'wb') as f:
            payload = part.get_payload(decode=True)
            if payload:
                f.write(payload)

    @staticmethod
    def _save_text_content(
        msg: email.message.Message, 
        path: str,
        valid_subject: str
    ) -> None:
        """保存非多部分邮件的文本内容
        
        Args:
            msg: 邮件消息对象
            path: 保存路径
            valid_subject: 有效主题
        """
        txt_filepath = os.path.join(path, f'{valid_subject}.txt')
        charset = msg.get_charset()
        if not charset:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        content = msg.get_payload(decode=True).decode(charset or 'utf-8')
        with open(txt_filepath, 'w', encoding='UTF-8') as f:
            f.write(content)

    @staticmethod
    def _check_resume_data(email_address: str) -> Optional[Dict]:
        """检查是否有未完成的下载数据
        
        Args:
            email_address: 邮箱地址
            
        Returns:
            dict: 包含已完成和失败邮件ID的字典，如果没有则返回None
        """
        resume_file = Path(f'./downloads/{email_address}/resume.json')
        if resume_file.exists():
            try:
                with open(resume_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"读取断点续传文件失败: {e}")
        return None

    @staticmethod
    def _update_resume_data(
        email_address: str, 
        email_id: bytes, 
        success: bool
    ) -> None:
        """更新断点续传数据
        
        Args:
            email_address: 邮箱地址
            email_id: 邮件ID
            success: 是否成功下载
        """
        resume_file = Path(f'./downloads/{email_address}/resume.json')
        try:
            data = {'completed': [], 'failed': []}
            if resume_file.exists():
                with open(resume_file, 'r') as f:
                    data = json.load(f)
            
            key = 'completed' if success else 'failed'
            data[key].append(email_id.decode('utf-8'))
            
            with open(resume_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"更新断点续传数据失败: {e}")

    @staticmethod
    def _save_attachment(
        part: email.message.Message, 
        path: str, 
        ui: Any,
        progress_callback: Optional[Callable[[], None]] = None
    ) -> bool:
        """保存邮件附件
        
        Args:
            part: 邮件部分对象
            path: 保存路径
            ui: 用户界面对象
            
        Returns:
            bool: 是否成功保存附件
        """
        filename = part.get_filename()
        if not filename:
            return False

        decode_filename, decode = email.header.decode_header(filename)[0]
        if isinstance(decode_filename, bytes):
            decode_filename = decode_filename.decode(decode or 'utf-8')

        content = part.get_payload(decode=True)
        if not content:
            return False

        filepath = os.path.join(path, decode_filename)
        with open(filepath, 'wb') as f:
            # 分块写入大文件
            chunk_size = 1024 * 1024  # 1MB
            for i in range(0, len(content), chunk_size):
                f.write(content[i:i+chunk_size])
                if ui and hasattr(ui, 'progressBar'):
                    QApplication.processEvents()  # 保持UI响应



class DownloadThread(QThread):
    """
    邮件下载线程类，负责在后台执行邮件下载任务
    """
    """邮件下载线程类
    
    Signals:
        progress_signal (int): 进度信号
        error_signal (str): 错误信号
    """
    progress_signal = pyqtSignal(int)
    error_signal = pyqtSignal(str)

    def __init__(self, email_address: str, password: str, ui: Any):
        """初始化下载线程
        
        Args:
            email_address: 邮箱地址
            password: 邮箱密码
            ui: 用户界面对象
        """
        super().__init__()
        self.email_address = email_address
        self.password = password
        self.ui = ui
        self.progress = ProgressSignal()
        self.progress.progress.connect(self.progress_signal)
        self.progress.error_occurred.connect(self.error_signal)

    def run(self):
        """线程主函数"""
        try:
            EmailDownload.download_emails(
                self.email_address, 
                self.password, 
                self.ui, 
                self.progress
            )
        except Exception as e:
            self.error_signal.emit(f"下载失败: {str(e)}")
            logger.error(f"下载线程错误: {e}")
        finally:
            self.progress_signal.emit(100)

class EmailDownloadUI(QMainWindow, ui_EmailDownload.Ui_MainWindow):
    """
    邮件下载主界面类，负责用户交互和下载控制
    """
    """邮件下载用户界面类"""
    
    def __init__(self):
        """初始化用户界面"""
        super(EmailDownloadUI, self).__init__()
        self.setupUi(self)
        self.load_credentials()
        self.confirm.clicked.connect(self.download)
        self._setup_connections()
        
    def _setup_connections(self):
        """设置信号连接"""
        self.mailAddress.textChanged.connect(self._validate_inputs)
        self.imapPassword.textChanged.connect(self._validate_inputs)
        
    def _validate_inputs(self):
        """验证输入是否有效"""
        email = self.mailAddress.text()
        password = self.imapPassword.text()
        valid = bool(email) and bool(password)
        self.confirm.setEnabled(valid)

    def closeEvent(self, event):
        self.save_credentials(self.mailAddress.text(), self.imapPassword.text())
        event.accept()
    
    def changeTitle(self, title):
        self.setWindowTitle(title)
    
    def save_credentials(self, email_address, password):
        credentials = {
            "email_address": email_address if self.checkBox.isChecked() else "example@example.com",
            "password": password if self.checkBox_2.isChecked() else "Your Password",
            "email_address_check": self.checkBox.isChecked(),
            "password_check": self.checkBox_2.isChecked(),
            "downloadHTML": self.downloadHTML.isChecked(),
            "seenAfterDownload": self.seenAfterDownload.isChecked(),
            "resumeDownload": self.resumeDownload.isChecked()
        }
        with open("credentials.json", "w") as f:
            json.dump(credentials, f)

    def load_credentials(self):
        if os.path.exists("credentials.json"):
            with open("credentials.json", "r") as f:
                credentials = json.load(f)
                self.mailAddress.setText(credentials.get("email_address", ""))
                self.imapPassword.setText(credentials.get("password", ""))
                self.checkBox.setChecked(credentials.get("email_address_check", False))
                self.checkBox_2.setChecked(credentials.get("password_check", False))
                self.downloadHTML.setChecked(credentials.get("downloadHTML", False))
                self.seenAfterDownload.setChecked(credentials.get("seenAfterDownload", False))
                self.resumeDownload.setChecked(credentials.get("resumeDownload", True))

    def download(self):
        self.confirm.setProperty("status", "loading")
        self.confirm.setEnabled(False)
        self.confirm.style().unpolish(self.confirm)
        self.confirm.style().polish(self.confirm)
        
        self.setWindowTitle("Email Download Tool | Downloading -- By Himalaya")

        email_address = self.mailAddress.text()
        password = self.imapPassword.text()
        self.progressBar.setValue(0)

        self.thread = DownloadThread(email_address, password, self)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.finished.connect(self.on_download_finished)
        self.thread.start()
        
    def update_progress(self, value):
        self.progressBar.setValue(value)
        QApplication.processEvents()  # 保持UI响应

    def on_download_finished(self):
        self.confirm.setProperty("status", "")
        self.confirm.setEnabled(True)
        self.confirm.style().unpolish(self.confirm)
        self.confirm.style().polish(self.confirm)

if __name__ == '__main__':
    QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mainWindow = EmailDownloadUI()
    mainWindow.setWindowIcon(QIcon("icon_rounded.png"))
    mainWindow.setWindowTitle("Email Download Tool | Waiting -- By Himalaya")
    mainWindow.show()
    sys.exit(app.exec_())
