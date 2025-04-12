# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# import time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(480, 480)
        MainWindow.setMinimumSize(480, 480)
        
        # 主窗口样式
        MainWindow.setStyleSheet(u"""
            QMainWindow {
                background-color: #f0f2f5;
                border: 1px solid #ddd;
                border-radius: 16px;
            }
            QMainWindow:hover {
                border: 2px solid #4CAF50;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: 500;
                background-color: white;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 3px;
                padding: 5px;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 13px;
                border-radius: 6px;
                min-width: 100px;
                transition: all 0.2s ease;
                font-weight: 500;
                position: relative;
                overflow: hidden;
            }
            QPushButton:hover {
                background-color: #45a049;
                padding: 12px 22px;
                font-size: 14px;
            }
            QPushButton:pressed {
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton::before {
                content: "";
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.2),
                    transparent
                );
                transition: 0.5s;
            }
            QPushButton:hover::before {
                left: 100%;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                transform: none;
                box-shadow: none;
            }
            QCheckBox {
                font-size: 12px;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0.5, x2:1, y2:0.5,
                    stop:0 #4CAF50, stop:0.5 #43A047, stop:1 #2E7D32
                );
                border-radius: 5px;
                width: 10px;
                margin: 1px;
            }
        """)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        
        # 主布局
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(20, 20, 20, 20)
        self.mainLayout.setSpacing(15)

        # 登录信息分组
        self.loginGroup = QGroupBox(u"登录信息")
        self.loginGroup.setStyleSheet("QGroupBox { font-size: 13px; }")
        self.loginLayout = QVBoxLayout(self.loginGroup)
        self.loginLayout.setContentsMargins(15, 15, 15, 15)
        self.loginLayout.setSpacing(12)
        
        # 邮箱地址行
        self.emailLayout = QHBoxLayout()
        self.emailLayout.setSpacing(8)
        
        self.mailAddress_Lab = QLabel(u"邮箱地址:", self.centralwidget)
        self.mailAddress_Lab.setFixedWidth(80)
        
        self.mailAddress = QLineEdit(self.centralwidget)
        self.mailAddress.setPlaceholderText(u"请输入邮箱地址")
        self.mailAddress.setClearButtonEnabled(True)
        self.mailAddress.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px 12px;
                background-color: white;
                color: #333;
                transition: all 0.2s ease;
                font-size: 13px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                position: relative;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background-color: #f8fff8;
            }
            QLineEdit:hover {
                border-color: #4CAF50;
                background-color: #f8fff8;
            }
            QLineEdit::placeholder {
                color: #aaa;
                font-style: italic;
            }
        """)
        
        self.checkBox = QCheckBox(u"记住邮箱地址", self.centralwidget)
        
        self.emailLayout.addWidget(self.mailAddress_Lab)
        self.emailLayout.addWidget(self.mailAddress)
        self.emailLayout.addWidget(self.checkBox)
        
        # 密码行
        self.passwordLayout = QHBoxLayout()
        self.passwordLayout.setSpacing(8)
        
        self.imapPassword_Lab = QLabel(u"IMAP密码:", self.centralwidget)
        self.imapPassword_Lab.setFixedWidth(80)
        
        self.imapPassword = QLineEdit(self.centralwidget)
        self.imapPassword.setPlaceholderText(u"请输入IMAP密码")
        self.imapPassword.setEchoMode(QLineEdit.Password)
        self.imapPassword.setClearButtonEnabled(True)
        self.imapPassword.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 10px 12px;
                background-color: white;
                color: #333;
                transition: all 0.2s ease;
                font-size: 13px;
                font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
                position: relative;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                outline: none;
                background-color: #f8fff8;
                padding: 11px 13px;
            }
            QLineEdit:hover {
                border-color: #4CAF50;
                background-color: #f8fff8;
            }
            QLineEdit::placeholder {
                color: #aaa;
                font-style: italic;
            }
        """)
        
        self.checkBox_2 = QCheckBox(u"记住密码", self.centralwidget)
        
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
        
        self.optionsRow1.addWidget(self.downloadHTML)
        self.optionsRow1.addWidget(self.seenAfterDownload)
        self.optionsRow1.addWidget(self.resumeDownload)
        self.optionsRow1.addStretch()
        
        # 统计信息
        self.statsLayout = QHBoxLayout()
        self.statsLayout.setSpacing(15)
        
        self.totalLabel = QLabel(u"邮件总数: 0", self.centralwidget)
        self.downloadedLabel = QLabel(u"已下载: 0", self.centralwidget)
        self.resumeLabel = QLabel(u"可续传: 0", self.centralwidget)
        self.resumeLabel.setToolTip(u"可从中断处继续下载的邮件数量")
        
        self.statsLayout.addWidget(self.totalLabel)
        self.statsLayout.addWidget(self.downloadedLabel)
        self.statsLayout.addWidget(self.resumeLabel)
        self.statsLayout.addStretch()
        
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
        self.progressBar.setStyleSheet("""
            QProgressBar {
                height: 24px;
                text-align: center;
                border-radius: 12px;
                border: 1px solid #ccc;
                background-color: #f8f9fa;
                font-size: 12px;
                min-width: 200px;
                padding: 1px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    spread:pad,
                    x1:0, y1:0.5, x2:1, y2:0.5,
                    stop:0 #4CAF50, stop:0.5 #43A047, stop:1 #2E7D32
                );
                border-radius: 12px;
                width: 10px;
                margin: 0.5px;
            }
            QProgressBar::chunk:first {
                border-top-left-radius: 12px;
                border-bottom-left-radius: 12px;
            }
            QProgressBar::chunk:last {
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
            }
        """)
        
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setContentsMargins(0, 10, 0, 0)
        self.buttonLayout.setSpacing(15)
        
        self.themeButton = QPushButton(u"🌙 暗色主题", self.centralwidget)
        self.themeButton.setFixedWidth(120)
        self.themeButton.setFixedHeight(36)
        self.themeButton.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 13px;
                border-radius: 6px;
                min-width: 120px;
                transition: all 0.2s;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #5a6268;
                padding: 11px 21px;
            }
            QPushButton:pressed {
                padding: 9px 19px;
            }
        """)
        self.themeButton.clicked.connect(self.toggle_theme)
        
        self.confirm = QPushButton(u"开始下载", self.centralwidget)
        self.confirm.setFixedWidth(150)
        self.confirm.setFixedHeight(36)
        self.confirm.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 6px;
                min-width: 120px;
                transition: all 0.2s;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #45a049;
                padding: 12px 22px;
                font-size: 14px;
            }
            QPushButton:pressed {
                padding: 10px 20px;
                font-size: 13px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                transform: none;
                box-shadow: none;
            }
            QPushButton[status="loading"] {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 120px;
            }
            QPushButton[status="loading"]::after {
                content: "";
                display: inline-block;
                width: 14px;
                height: 14px;
                margin-left: 8px;
                border: 3px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 1s ease-in-out infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        """)
        
        self.buttonLayout.addWidget(self.themeButton)
        self.buttonLayout.addWidget(self.confirm)
        
        self.progressLayout.addWidget(self.progressBar)
        self.progressLayout.addLayout(self.buttonLayout)

        # 添加到主布局
        self.mainLayout.addWidget(self.loginGroup)
        self.mainLayout.addWidget(self.optionsGroup)
        self.mainLayout.addWidget(self.progressGroup)

        MainWindow.setCentralWidget(self.centralwidget)

    def toggle_theme(self):
        """切换明暗主题"""
        current_text = self.themeButton.text()
        if "🌙" in current_text:
            # 切换到暗色主题
            self.themeButton.setText("☀️ 亮色主题")
            dark_theme = """
                QMainWindow {
                    background-color: #2d2d2d;
                    border: 1px solid #444;
                }
                QGroupBox {
                    background-color: #3a3a3a;
                    border: 1px solid #444;
                    color: #eee;
                }
                QLabel, QCheckBox {
                    color: #eee;
                }
                QTextEdit, QLineEdit {
                    background-color: #3a3a3a;
                    color: #eee;
                    border: 1px solid #555;
                }
                QPushButton {
                    background-color: #4a6fa5;
                }
                QPushButton:hover {
                    background-color: #3d5d8c;
                }
                QProgressBar {
                    background-color: #3a3a3a;
                    border: 1px solid #555;
                }
            """
            self.centralwidget.setStyleSheet(dark_theme)
        else:
            # 切换回亮色主题
            self.themeButton.setText("🌙 暗色主题")
            self.centralwidget.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f2f5;
                    border: 1px solid #ddd;
                }
                QGroupBox {
                    background-color: white;
                    border: 1px solid #ddd;
                    color: #333;
                }
                QLabel, QCheckBox {
                    color: #333;
                }
                QTextEdit, QLineEdit {
                    background-color: white;
                    color: #333;
                    border: 1px solid #ddd;
                }
                QPushButton {
                    background-color: #4CAF50;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QProgressBar {
                    background-color: #f8f9fa;
                    border: 1px solid #ccc;
                }
            """)
