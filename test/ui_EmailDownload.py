from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QFileDialog, 
                            QGroupBox, QCheckBox, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QFile, QTextStream, QPropertyAnimation
from PyQt5.QtGui import QIcon
import sys
import os
import json
import imaplib
import email
import email.header
from datetime import datetime
from email.utils import parsedate_to_datetime, parseaddr
from email.header import make_header, decode_header

class DownloadThread(QThread):
    progress_updated = pyqtSignal(int, int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = parent
        self.running = True
        
    def run(self):
        try:
            email_address = self.ui.mailAddress.text()
            password = self.ui.imapPassword.text()
            
            if not email_address or not password:
                self.finished.emit(False, "邮箱地址和密码不能为空")
                return
                
            # 获取IMAP服务器配置
            with open("imap_servers.json", "r") as f:
                imap_servers = json.load(f)
                
            domain = email_address.split('@')[-1]
            imap_server = imap_servers.get(domain, None)
            
            if not imap_server:
                self.finished.emit(False, f"不支持{domain}域名的邮箱")
                return
                
            # 连接IMAP服务器
            mail = imaplib.IMAP4_SSL(imap_server)
            mail.login(email_address, password)
            mail.select('inbox')
            
            # 获取邮件总数
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                self.finished.emit(False, "获取邮件列表失败")
                return
                
            messages = messages[0].split()
            total = len(messages)
            self.progress_updated.emit(0, total, "开始下载...")
            
            # 下载邮件
            for i, msg_id in enumerate(messages):
                if not self.running:
                    break
                    
                status, data = mail.fetch(msg_id, '(RFC822)')
                if status != 'OK':
                    continue
                    
                raw_email = data[0][1]
                email_message = email.message_from_bytes(raw_email)
                
                # 保存邮件到本地
                self.save_email(email_message, email_address)
                
                # 更新进度
                self.progress_updated.emit(i+1, total, f"正在下载 {i+1}/{total}")
                
            mail.close()
            mail.logout()
            self.finished.emit(True, f"成功下载 {len(messages)} 封邮件")
            
        except Exception as e:
            self.finished.emit(False, f"下载失败: {str(e)}")
            
    def save_email(self, email_message, email_address):
        """保存邮件到本地"""
        email_dir = os.path.join("emails", email_address.split('@')[0])
        if not os.path.exists(email_dir):
            os.makedirs(email_dir)
            
        # 生成唯一文件名
        msg_id = email_message.get('Message-ID', '').strip('<>') or str(int(datetime.now().timestamp()))
        filename = f"{msg_id}.eml"
        
        # 保存邮件主体
        with open(os.path.join(email_dir, filename), 'wb') as f:
            f.write(email_message.as_bytes())
            
        # 处理附件
        if self.ui.downloadAttachments.isChecked():
            attachments_dir = os.path.join(email_dir, "attachments")
            if not os.path.exists(attachments_dir):
                os.makedirs(attachments_dir)
                
            for part in email_message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue
                    
                filename = part.get_filename()
                if filename:
                    filepath = os.path.join(attachments_dir, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
            
    def stop(self):
        """停止下载"""
        self.running = False

class EmailDownloadUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("邮箱下载器")
        self.setFixedSize(400, 300)
        
        # 中央部件
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        
        # 主布局
        self.mainLayout = QVBoxLayout(self.centralwidget)
        
        # 邮箱地址部分
        self.mailLayout = QHBoxLayout()
        self.mailAddress_Lab = QLabel("邮箱地址:")
        self.mailAddress_Lab.setFixedWidth(90)
        self.mailAddress_Lab.setStyleSheet("font-weight: bold;")
        
        self.mailAddress = QLineEdit()
        self.mailAddress.setPlaceholderText("请输入邮箱地址")
        self.mailAddress.setClearButtonEnabled(True)
        
        self.mailLayout.addWidget(self.mailAddress_Lab)
        self.mailLayout.addWidget(self.mailAddress)
        
        # 密码部分
        self.passwordLayout = QHBoxLayout()
        self.imapPassword_Lab = QLabel("IMAP密码:")
        self.imapPassword_Lab.setFixedWidth(90)
        self.imapPassword_Lab.setStyleSheet("font-weight: bold;")
        
        self.imapPassword = QLineEdit()
        self.imapPassword.setPlaceholderText("请输入IMAP密码")
        self.imapPassword.setEchoMode(QLineEdit.Password)
        
        self.passwordLayout.addWidget(self.imapPassword_Lab)
        self.passwordLayout.addWidget(self.imapPassword)
        
        # 按钮部分
        self.buttonLayout = QHBoxLayout()
        self.downloadBtn = QPushButton("下载邮件")
        self.downloadBtn.setFixedHeight(40)
        self.downloadBtn.clicked.connect(self.start_download)
        
        self.buttonLayout.addWidget(self.downloadBtn)
        
        # 添加到主布局
        self.mainLayout.addLayout(self.mailLayout)
        self.mainLayout.addLayout(self.passwordLayout)
        self.mainLayout.addLayout(self.buttonLayout)
        self.mainLayout.addStretch()

    def setupUi(self, MainWindow: QMainWindow) -> None:
        """初始化主窗口UI"""
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(650, 350)
        MainWindow.setMinimumSize(550, 300)
        
        self.centralwidget = QWidget(MainWindow)
        self.load_stylesheet("light")
        self.centralwidget.setObjectName(u"centralwidget")
        
        # 主布局
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(25, 25, 25, 25)
        self.mainLayout.setSpacing(20)

        # 登录信息分组
        self.loginGroup = QGroupBox(u"登录信息")
        self.loginGroup.setStyleSheet("""
            QGroupBox { 
                font-size: 14px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        self.loginLayout = QVBoxLayout(self.loginGroup)
        self.loginLayout.setContentsMargins(20, 25, 20, 20)
        self.loginLayout.setSpacing(15)
        
        # 邮箱地址行
        self.emailLayout = QHBoxLayout()
        self.emailLayout.setSpacing(8)
        
        self.mailAddress_Lab = QLabel(u"邮箱地址:", self.centralwidget)
        self.mailAddress_Lab.setFixedWidth(90)
        self.mailAddress_Lab.setStyleSheet("font-weight: bold;")
        
        self.mailAddress = QLineEdit(self.centralwidget)
        self.mailAddress.setPlaceholderText(u"请输入邮箱地址")
        self.mailAddress.setClearButtonEnabled(True)
        
        self.checkBox = QCheckBox(u"记住邮箱地址", self.centralwidget)
        self.checkBox.stateChanged.connect(self.save_credentials)
        
        self.emailLayout.addWidget(self.mailAddress_Lab)
        self.emailLayout.addWidget(self.mailAddress)
        self.emailLayout.addWidget(self.checkBox)
        
        # 密码行
        self.passwordLayout = QHBoxLayout()
        self.passwordLayout.setSpacing(8)
        
        self.imapPassword_Lab = QLabel(u"IMAP密码:", self.centralwidget)
        self.imapPassword_Lab.setFixedWidth(90)
        self.imapPassword_Lab.setStyleSheet("font-weight: bold;")
        
        self.imapPassword = QLineEdit(self.centralwidget)
        self.imapPassword.setPlaceholderText(u"请输入IMAP密码")
        self.imapPassword.setEchoMode(QLineEdit.Password)
        self.imapPassword.setClearButtonEnabled(True)
        
        self.checkBox_2 = QCheckBox(u"记住密码", self.centralwidget)
        self.checkBox_2.stateChanged.connect(self.save_credentials)
        
        self.passwordLayout.addWidget(self.imapPassword_Lab)
        self.passwordLayout.addWidget(self.imapPassword)
        self.passwordLayout.addWidget(self.checkBox_2)

        # 添加到登录分组
        self.loginLayout.addLayout(self.emailLayout)
        self.loginLayout.addLayout(self.passwordLayout)
        
        # 选项分组
        self.optionsGroup = QGroupBox(u"下载选项")
        self.optionsGroup.setStyleSheet("QGroupBox { font-size: 13px; }")
        self.optionsLayout = QVBoxLayout(self.optionsGroup)
        self.optionsLayout.setContentsMargins(15, 15, 15, 15)
        self.optionsLayout.setSpacing(12)
        
        # 第一行选项
        self.optionsRow1 = QHBoxLayout()
        self.optionsRow1.setSpacing(15)
        
        self.downloadHTML = QCheckBox(u"下载HTML内容", self.centralwidget)
        self.downloadHTML.setToolTip(u"同时下载邮件的HTML格式内容")
        
        self.seenAfterDownload = QCheckBox(u"下载后标记为已读", self.centralwidget)
        self.seenAfterDownload.setToolTip(u"下载完成后将邮件标记为已读状态")
        
        self.resumeDownload = QCheckBox(u"断点续传", self.centralwidget)
        self.resumeDownload.setToolTip(u"支持从中断处继续下载未完成的邮件")
        self.resumeDownload.setChecked(True)

        self.downloadAttachments = QCheckBox(u"下载附件", self.centralwidget)
        self.downloadAttachments.setToolTip(u"下载邮件中的附件文件")
        self.downloadAttachments.setChecked(True)
        
        self.optionsRow1.addWidget(self.downloadHTML)
        self.optionsRow1.addWidget(self.seenAfterDownload)
        self.optionsRow1.addWidget(self.resumeDownload)
        self.optionsRow1.addWidget(self.downloadAttachments)
        self.optionsRow1.addStretch()
        
        # 统计信息
        self.statsLayout = QGridLayout()
        self.statsLayout.setHorizontalSpacing(20)
        self.statsLayout.setVerticalSpacing(8)
        
        self.totalLabel = QLabel(u"邮件总数: 0", self.centralwidget)
        self.downloadedLabel = QLabel(u"已下载: 0", self.centralwidget)
        self.resumeLabel = QLabel(u"可续传: 0", self.centralwidget)
        self.resumeLabel.setToolTip(u"可从中断处继续下载的邮件数量")
        self.attachmentsLabel = QLabel(u"附件数: 0", self.centralwidget)
        self.attachmentsLabel.setToolTip(u"待下载的附件数量")
        
        self.statsLayout.addWidget(self.totalLabel, 0, 0)
        self.statsLayout.addWidget(self.downloadedLabel, 0, 1)
        self.statsLayout.addWidget(self.resumeLabel, 1, 0)
        self.statsLayout.addWidget(self.attachmentsLabel, 1, 1)
        
        self.optionsLayout.addLayout(self.optionsRow1)
        self.optionsLayout.addLayout(self.statsLayout)

        # 进度条和按钮
        self.progressGroup = QGroupBox(u"下载进度")
        self.progressGroup.setStyleSheet("QGroupBox { font-size: 13px; }")
        self.progressLayout = QVBoxLayout(self.progressGroup)
        self.progressLayout.setContentsMargins(15, 15, 15, 15)
        self.progressLayout.setSpacing(12)
        
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setValue(0)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat("%p% (%v/%m)")
        self.progressBar.setObjectName("mainProgress")
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(0, 10, 0, 0)
        self.buttonLayout.setSpacing(15)
        
        self.themeButton = QPushButton(u"🌙 暗色主题", self.centralwidget)
        self.themeButton.setObjectName("themeButton")
        self.themeButton.setFixedWidth(120)
        self.themeButton.setFixedHeight(36)
        self.themeButton.clicked.connect(self.toggle_theme)
        
        self.confirm = QPushButton(u"开始下载", self.centralwidget)
        self.confirm.setFixedWidth(150)
        self.confirm.setFixedHeight(36)
        self.confirm.clicked.connect(self.start_download)
        
        self.buttonLayout.addWidget(self.themeButton)
        self.buttonLayout.addWidget(self.confirm)
        
        self.progressLayout.addWidget(self.progressBar)
        self.progressLayout.addLayout(self.buttonLayout)

        # 添加到主布局
        self.mainLayout.addWidget(self.loginGroup)
        self.mainLayout.addWidget(self.optionsGroup)
        self.mainLayout.addWidget(self.progressGroup)

        MainWindow.setCentralWidget(self.centralwidget)
        self.load_credentials()

    def start_download(self):
        """开始下载邮件"""
        self.download_thread = DownloadThread(self)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def update_progress(self, current, total, message):
        """更新进度显示"""
        self.progressBar.setValue(int(current/total*100))
        self.progressBar.setFormat(message)
        self.downloadedLabel.setText(f"已下载: {current}")
        
        # 更新附件数量统计
        email_dir = os.path.join("emails", self.mailAddress.text().split('@')[0])
        attachments_dir = os.path.join(email_dir, "attachments")
        if os.path.exists(attachments_dir):
            attachment_count = len([f for f in os.listdir(attachments_dir) 
                                if os.path.isfile(os.path.join(attachments_dir, f))])
            self.attachmentsLabel.setText(f"附件数: {attachment_count}")
        
    def on_download_finished(self, success, message):
        """下载完成处理"""
        if success:
            QMessageBox.information(None, "完成", message)
        else:
            QMessageBox.critical(None, "错误", message)
        self.progressBar.setFormat("准备就绪")

    def load_stylesheet(self, theme: str) -> None:
        """加载并应用样式表"""
        try:
            style_file = QFile("styles.qss")
            if not style_file.exists():
                raise FileNotFoundError("样式表文件styles.qss不存在")
                
            if style_file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(style_file)
                stylesheet = stream.readAll()
                
                animation = QPropertyAnimation(self.centralwidget, b"windowOpacity")
                animation.setDuration(300)
                animation.setStartValue(0.7)
                animation.setEndValue(1.0)
                animation.start()
                
                if theme == "dark":
                    stylesheet = stylesheet.replace('[theme="light"]', '[theme="dark"]')
                else:
                    stylesheet = stylesheet.replace('[theme="dark"]', '[theme="light"]')
                
                widgets = QApplication.allWidgets()
                for widget in widgets:
                    widget.setProperty("theme", theme)
                    for child in widget.findChildren(QWidget):
                        child.setProperty("theme", theme)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                
                QApplication.instance().setStyleSheet(stylesheet)
                self.centralwidget.setStyleSheet(stylesheet)
                style_file.close()
                
                QApplication.instance().setStyle(QApplication.instance().style())
                self.log_message(f"主题已切换为: {theme}")
                
        except Exception as e:
            print(f"加载样式表失败: {e}")
            self.log_message(f"主题切换失败: {str(e)}", "WARNING")

    def toggle_theme(self):
        """切换明暗主题"""
        current_text = self.themeButton.text()
        if "🌙" in current_text:
            self.themeButton.setText("☀️ 亮色主题")
            theme = "dark"
        else:
            self.themeButton.setText("🌙 暗色主题")
            theme = "light"
        
        self.themeButton.setProperty("theme", theme)
        self.load_stylesheet(theme)
        
        try:
            config = {}
            if os.path.exists("credentials.json"):
                with open("credentials.json", "r") as f:
                    config = json.load(f)
            
            config["theme"] = theme
            
            with open("credentials.json", "w") as f:
                json.dump(config, f, indent=4)
                
            self.log_message(f"主题已切换为: {theme}")
        except Exception as e:
            print(f"保存主题配置失败: {e}")
            self.log_message(f"主题保存失败: {str(e)}")

    def save_credentials(self):
        """保存邮箱和密码到credentials.json"""
        try:
            if os.path.exists("credentials.json"):
                if not os.access("credentials.json", os.W_OK):
                    raise PermissionError("没有写入credentials.json的权限")
                
                backup_path = "credentials.json.bak"
                if os.path.exists(backup_path):
                    os.remove(backup_path)
                os.rename("credentials.json", backup_path)
            
            credentials = {}
            if os.path.exists("credentials.json.bak"):
                try:
                    with open("credentials.json.bak", "r") as f:
                        credentials = json.load(f)
                except json.JSONDecodeError:
                    credentials = {}
            
            new_credentials = {
                "email_address": self.mailAddress.text(),
                "password": self.imapPassword.text(),
                "email_address_check": self.checkBox.isChecked(),
                "password_check": self.checkBox_2.isChecked(),
                "downloadHTML": self.downloadHTML.isChecked(),
                "seenAfterDownload": self.seenAfterDownload.isChecked(),
                "resumeDownload": self.resumeDownload.isChecked(),
                "downloadAttachments": self.downloadAttachments.isChecked()
            }
            
            credentials.update(new_credentials)
            
            if "email" in credentials:
                del credentials["email"]
            
            if not self.checkBox_2.isChecked():
                credentials["password"] = ""
            else:
                try:
                    from cryptography.fernet import Fernet
                    if "password_key" not in credentials:
                        key = Fernet.generate_key()
                        credentials["password_key"] = key.decode()
                    else:
                        key = credentials["password_key"].encode()
                    
                    cipher_suite = Fernet(key)
                    encrypted_pwd = cipher_suite.encrypt(self.imapPassword.text().encode())
                    credentials["password"] = f"enc:{encrypted_pwd.decode()}"
                except ImportError:
                    self.log_message("警告: cryptography模块未安装，密码将以明文保存", "WARNING")
                    credentials["password"] = self.imapPassword.text()
                except Exception as e:
                    self.log_message(f"密码加密失败: {str(e)}", "WARNING")
                    credentials["password"] = self.imapPassword.text()
            
            temp_path = "credentials.json.tmp"
            with open(temp_path, "w") as f:
                json.dump(credentials, f, indent=4)
            
            if os.path.exists("credentials.json"):
                os.remove("credentials.json")
            os.rename(temp_path, "credentials.json")
            
            self.log_message("凭据保存成功")
                
        except PermissionError as e:
            error_msg = f"文件权限错误: {str(e)}"
            QMessageBox.critical(None, "错误", error_msg)
            self.log_message(error_msg, "ERROR")
        except Exception as e:
            error_msg = f"保存凭据失败: {str(e)}"
            QMessageBox.critical(None, "错误", error_msg)
            self.log_message(error_msg)
            
            if os.path.exists("credentials.json.bak"):
                if os.path.exists("credentials.json"):
                    os.remove("credentials.json")
                os.rename("credentials.json.bak", "credentials.json")

    def log_message(self, message: str, level: str = "INFO") -> None:
        """记录日志消息到文件和控制台"""
        try:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            log_file = os.path.join(log_dir, "email_downloader.log")
            
            if os.path.exists(log_file) and os.path.getsize(log_file) > 5 * 1024 * 1024:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(log_dir, f"email_downloader_{timestamp}.log")
                os.rename(log_file, backup_file)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_msg = f"[{timestamp}] [{level}] {message}\n"
            
            # 写入日志文件
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_msg)
                
            # 打印到控制台(ERROR级别用红色显示)
            if level == "ERROR":
                print(f"\033[91m{log_msg.strip()}\033[0m")
            elif level == "WARNING":
                print(f"\033[93m{log_msg.strip()}\033[0m")
            else:
                print(log_msg.strip())
            
        except Exception as e:
            print(f"\033[91m日志记录失败: {e}\033[0m")
            print(f"\033[91m原始日志消息: [{level}] {message}\033[0m")
