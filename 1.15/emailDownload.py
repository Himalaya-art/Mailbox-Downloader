'''
邮箱下载工具
    GUI界面
    展示已读未读
    下载附件
    下载邮箱正文内容
'''

import email
import email.header
from email.utils import parseaddr
import imaplib
import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QObject, QThread, Qt, QPoint, QEvent, pyqtSignal
import datetime
import os
import re
import bs4
import ui_EmailDownload
from email.parser import BytesParser
import json
from datetime import datetime
from email.utils import parsedate_to_datetime
from email.header import make_header, decode_header
import time
from concurrent.futures import ThreadPoolExecutor
import threading
from threading import Thread

class Tools:
    @staticmethod
    def rename(email_id, msg, path):
        if msg['Date']:
            email_time = parsedate_to_datetime(msg['Date']).strftime('%Y-%m-%d %H-%M-%S')
            path = f"{path}_{email_time}_{email_id.decode('utf-8')}"
        else:
            path = f"{path}_{email_id.decode('utf-8')}"
        return path

class ProgressSignal(QObject):
    progress = pyqtSignal(int)

class EmailDownload:
    @staticmethod
    def download_emails(email_address: str, password: str, ui, progress_signal):
        try:
            domain = email_address.split("@")[1]
            imap_servers = {
                "qq.com": "imap.qq.com",
                "gmail.com": "imap.gmail.com",
                "163.com": "imap.163.com",
                "outlook.com": "imap-mail.outlook.com"
            }
            mail_server = imap_servers.get(domain, f"imap.{domain}")
            mail = imaplib.IMAP4_SSL(mail_server, timeout=30)
            mail.login(email_address, password)
            mail.select("INBOX")
            status, email_ids = mail.search(None, 'UNSEEN')
            email_list = email_ids[0].split()
            mail.close()
            mail.logout()
    
            if not email_list:
                ui.changeTitle('Email Download Tool | No unread emails -- By Himalaya')
                return
    
            total = len(email_list)
            completed = 0
            lock = threading.Lock()
    
            def update_progress():
                nonlocal completed
                with lock:
                    completed += 1
                    progress = int((completed / total) * 100)
                    progress_signal.emit(progress)
    
            for idx, email_id in enumerate(email_list):
                EmailDownload.download_email(
                    email_id, email_address, password, ui, update_progress
                )
                progress = int((idx + 1) / len(email_list) * 100)
                progress_signal.emit(progress)
    
            ui.changeTitle('Email Download Tool | Done! -- By Himalaya')
    
        except Exception as e:
            print(f"Error in download_emails: {str(e)}")
            ui.changeTitle('Email Download Tool | Error -- By Himalaya')
    
    @staticmethod
    def download_email(email_id, email_address, password, ui, progress_callback):
        retry_count = 3
        mail = None
        
        for attempt in range(retry_count):
            try:
                domain = email_address.split("@")[1]
                imap_servers = {
                    "qq.com": "imap.qq.com",
                    "gmail.com": "imap.gmail.com",
                    "163.com": "imap.163.com",
                    "outlook.com": "imap-mail.outlook.com"
                }
                mail_server = imap_servers.get(domain, f"imap.{domain}")
                mail = imaplib.IMAP4_SSL(mail_server, timeout=30)
                mail.login(email_address, password)
                mail.select("INBOX")

                msg = BytesParser().parsebytes(mail.fetch(email_id, '(RFC822)')[1][0][1])
                break
            except (imaplib.IMAP4.abort, ConnectionError) as e:
                if attempt < retry_count - 1:
                    time.sleep(2)
                    try:
                        if mail:
                            mail.close()
                            mail.logout()
                    except:
                        pass
                    continue
                else:
                    print(f"Failed to download email after {retry_count} attempts: {str(e)}")
                    return
            finally:
                try:
                    if mail:
                        mail.close()
                        mail.logout()
                except:
                    pass

        subject = make_header(decode_header(msg['SUBJECT']))
        subject = re.sub(r'[\\/:*?"<>|]', '', str(subject)).strip()

        if not subject or subject.isspace():
            valid_subject = f'无主题_{int(time.time())}'
        else:
            valid_subject = subject

        path = f'./{valid_subject}'
        path = Tools.rename(email_id, msg, path)

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain':
                    txt_filepath = os.path.join(path, f'{valid_subject}.txt')
                    content = part.get_payload(decode=True).decode(part.get_content_charset())
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(txt_filepath, 'w', encoding='UTF-8') as f:
                        f.write(content)
                elif content_type == 'text/html' and ui.downloadHTML.isChecked():
                    html_filepath = os.path.join(path, f'{valid_subject}.html')
                    content = part.get_payload(decode=True).decode(part.get_content_charset())
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(html_filepath, 'w', encoding='UTF-8') as f:
                        f.write(content)
                elif 'image' in content_type:
                    image_filepath = os.path.join(path, f'{valid_subject}.{content_type.split("/")[1]}')
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(image_filepath, 'wb') as f:
                        payload = part.get_payload(decode=True)
                        if payload:
                            f.write(payload)
        else:
            txt_filepath = os.path.join(path, f'{valid_subject}.txt')
            charset = msg.get_charset()
            if not charset:
                content_type = msg.get('Content-Type', '').lower()
                pos = content_type.find('charset=')
                if pos >= 0:
                    charset = content_type[pos + 8:].strip()
            content = msg.get_payload(decode=True).decode(charset or 'utf-8')
            if not os.path.exists(path):
                os.makedirs(path)
            with open(txt_filepath, 'w', encoding='UTF-8') as f:
                f.write(content)

        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get("Content-Disposition") is None:
                continue

            filename = part.get_filename()
            if filename:
                decode_filename, decode = email.header.decode_header(filename)[0]
                if isinstance(decode_filename, bytes):
                    decode_filename = decode_filename.decode(decode)

                content = part.get_payload(decode=True)
                filepath = os.path.join(path, decode_filename)
                os.makedirs(path, exist_ok=True)

                with open(filepath, 'wb') as f:
                    if content:
                        # 分块写入大文件
                        chunk_size = 1024 * 1024  # 1MB
                        for i in range(0, len(content), chunk_size):
                            f.write(content[i:i+chunk_size])
                            if ui and hasattr(ui, 'progressBar'):
                                QApplication.processEvents()  # 保持UI响应

        if progress_callback:
            progress_callback()

        if ui.seenAfterDownload.isChecked() and mail:
            try:
                mail.select("INBOX")
                mail.store(email_id, '+FLAGS', '\\Seen')
            except Exception as e:
                print(f"标记邮件失败: {str(e)}")

class DownloadThread(QThread):
    progress_signal = pyqtSignal(int)

    def __init__(self, email_address, password, ui):
        super().__init__()
        self.email_address = email_address
        self.password = password
        self.ui = ui

    def run(self):
        try:
            EmailDownload.download_emails(self.email_address, self.password, self.ui, self.progress_signal)
        finally:
            self.progress_signal.emit(100)

class EmailDownloadUI(QMainWindow, ui_EmailDownload.Ui_MainWindow):
    def __init__(self):
        super(EmailDownloadUI, self).__init__()
        self.setupUi(self)
        self.load_credentials()
        self.confirm.clicked.connect(self.download)

    def closeEvent(self, event):
        self.save_credentials(self.mailAddress.toPlainText(), self.imapPassword.toPlainText())
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
            "seenAfterDownload": self.seenAfterDownload.isChecked()
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

    def download(self):
        self.confirm.setEnabled(False)
        self.setWindowTitle("Email Download Tool | Downloading -- By Himalaya")

        email_address = self.mailAddress.toPlainText()
        password = self.imapPassword.toPlainText()
        self.progressBar.setValue(0)

        self.thread = DownloadThread(email_address, password, self)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.finished.connect(self.on_download_finished)
        self.thread.start()
        
    def update_progress(self, value):
        self.progressBar.setValue(value)
        QApplication.processEvents()  # 保持UI响应

    def on_download_finished(self):
        self.confirm.setEnabled(True)

if __name__ == '__main__':
    QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    mainWindow = EmailDownloadUI()
    mainWindow.setWindowIcon(QIcon("icon.png"))
    mainWindow.setWindowTitle("Email Download Tool | Waiting -- By Himalaya")
    mainWindow.show()
    sys.exit(app.exec_())
