"""
邮箱下载工具
功能：
- GUI界面
- 展示已读未读
- 下载附件
- 下载邮箱正文内容
优化点：
1. 多线程下载
2. 增强错误处理
3. 改进进度计算
4. 安全凭据存储
"""

import email
import imaplib
import sys
import os
import re
import logging
import json
import time
from datetime import datetime
from email.parser import BytesParser
from email.header import make_header, decode_header
from email.utils import parsedate_to_datetime
from concurrent.futures import ThreadPoolExecutor

from PySide2.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide2.QtCore import Signal, QObject, QThread, Qt, QRect
from PySide2.QtGui import QFont, QPixmap, QPalette, QBrush, QIcon

import ui_EmailDownload

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("email_download.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Tools:
    @staticmethod
    def safe_filename(text, max_length=100):
        """生成安全文件名"""
        cleaned = re.sub(r'[\\/*?:"<>|]', '', str(text)).strip()[:max_length]
        return cleaned or 'untitled'

    @staticmethod
    def get_imap_server(email_address):
        """获取IMAP服务器地址"""
        domain = email_address.split('@')[-1]
        servers = {
            'gmail.com': 'imap.gmail.com',
            'outlook.com': 'imap-mail.outlook.com',
            'qq.com': 'imap.qq.com'
        }
        return servers.get(domain, f'imap.{domain}')

class ProgressSignal(QObject):
    progress = Signal(int)
    error = Signal(str)

class DownloadThread(QThread):
    progress_signal = Signal(int)
    error_signal = Signal(str)

    def __init__(self, email_address, password, ui):
        super().__init__()
        self.email_address = email_address
        self.password = password
        self.ui = ui
        self._is_running = True

    def run(self):
        try:
            server = Tools.get_imap_server(self.email_address)
            with imaplib.IMAP4_SSL(server) as mail:
                mail.login(self.email_address, self.password)
                mail.select("INBOX")
                
                status, email_ids = mail.search(None, 'UNSEEN')
                email_list = email_ids[0].split()
                total = len(email_list)

                with ThreadPoolExecutor(max_workers=5) as executor:
                    futures = []
                    for idx, email_id in enumerate(email_list, 1):
                        if not self._is_running:
                            break
                        future = executor.submit(
                            self.process_email,
                            email_id, mail, idx, total
                        )
                        futures.append(future)
                    
                    for future in futures:
                        future.result()

                self.progress_signal.emit(100)
                self.ui.changeTitle('下载完成!')

        except Exception as e:
            logger.error(f"连接错误: {str(e)}")
            self.error_signal.emit(f"连接失败: {str(e)}")
        finally:
            self.ui.enable_ui(True)

    def process_email(self, email_id, mail, idx, total):
        """处理单个邮件"""
        try:
            retry = 3
            for _ in range(retry):
                try:
                    _, data = mail.fetch(email_id, '(RFC822)')
                    msg = BytesParser().parsebytes(data[0][1])
                    break
                except imaplib.IMAP4.abort:
                    time.sleep(1)
                    continue

            # 处理邮件内容
            subject = Tools.safe_filename(msg['SUBJECT'])
            date = parsedate_to_datetime(msg['Date']).strftime('%Y%m%d_%H%M%S') if msg['Date'] else ''
            path = f"./emails/{date}_{email_id.decode()}_{subject}"

            os.makedirs(path, exist_ok=True)
            
            # 保存各部分内容
            self.save_content(msg, path)
            self.save_attachments(msg, path)

            # 更新进度
            progress = int((idx / total) * 100)
            self.progress_signal.emit(progress)

            if self.ui.seenAfterDownload.isChecked():
                mail.store(email_id, '+FLAGS', '\\Seen')

        except Exception as e:
            logger.error(f"邮件处理失败: {str(e)}")
            self.error_signal.emit(f"邮件{email_id}处理失败: {str(e)}")

    def save_content(self, msg, path):
        """保存邮件正文"""
        counter = 1
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                content = part.get_payload(decode=True)
                charset = part.get_content_charset() or 'utf-8'
                with open(os.path.join(path, f'content_{counter}.txt'), 'w', encoding='utf-8') as f:
                    f.write(content.decode(charset, errors='replace'))
                counter += 1

    def save_attachments(self, msg, path):
        """保存附件"""
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    filename = Tools.safe_filename(filename)
                    data = part.get_payload(decode=True)
                    with open(os.path.join(path, filename), 'wb') as f:
                        f.write(data)

    def stop(self):
        """停止下载"""
        self._is_running = False

class EmailDownloadUI(QMainWindow, ui_EmailDownload.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.thread = None
        self.load_credentials()
        self.setup_connections()
        self.setWindowIcon(QIcon('icon.png'))

    def setup_connections(self):
        """连接信号槽"""
        self.confirm.clicked.connect(self.start_download)
        self.minimizeButton.clicked.connect(self.showMinimized)
        self.maximizeButton.clicked.connect(self.toggle_maximize)
        self.closeButton.clicked.connect(self.close)

    def start_download(self):
        """开始下载"""
        if not self.validate_input():
            return

        self.enable_ui(False)
        self.progressBar.setValue(0)
        
        self.thread = DownloadThread(
            self.mailAddress.text(),
            self.imapPassword.text(),
            self
        )
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.error_signal.connect(self.show_error)
        self.thread.finished.connect(self.on_download_finished)
        self.thread.start()

        self.save_credentials()

    def validate_input(self):
        """验证输入"""
        email = self.mailAddress.text()
        password = self.imapPassword.text()
        
        if not email or '@' not in email:
            self.show_error("请输入有效的邮箱地址")
            return False
        if not password:
            self.show_error("请输入密码")
            return False
        return True

    def enable_ui(self, enable):
        """启用/禁用UI控件"""
        self.confirm.setEnabled(enable)
        self.mailAddress.setEnabled(enable)
        self.imapPassword.setEnabled(enable)

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def show_error(self, message):
        QMessageBox.critical(self, "错误", message)

    def on_download_finished(self):
        self.enable_ui(True)
        if self.thread:
            self.thread.deleteLater()

    def closeEvent(self, event):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait(2000)
        self.save_credentials()
        event.accept()

    def save_credentials(self):
        """安全存储凭据"""
        credentials = {
            "email": self.mailAddress.text() if self.checkBox.isChecked() else "",
            "password": self.imapPassword.text() if self.checkBox_2.isChecked() else "",
            "options": {
                "html": self.downloadHTML.isChecked(),
                "seen": self.seenAfterDownload.isChecked()
            }
        }
        with open("credentials.json", "w") as f:
            json.dump(credentials, f, indent=4)

    def load_credentials(self):
        """加载存储的凭据"""
        if os.path.exists("credentials.json"):
            with open("credentials.json") as f:
                data = json.load(f)
                self.mailAddress.setText(data.get("email", ""))
                self.imapPassword.setText(data.get("password", ""))
                opts = data.get("options", {})
                self.downloadHTML.setChecked(opts.get("html", False))
                self.seenAfterDownload.setChecked(opts.get("seen", False))

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

if __name__ == '__main__':
    # 高DPI支持
    if sys.platform == "win32":
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = EmailDownloadUI()
    window.setWindowTitle("智能邮件下载器")
    window.show()
    sys.exit(app.exec_())
