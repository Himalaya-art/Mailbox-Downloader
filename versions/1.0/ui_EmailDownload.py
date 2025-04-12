# -*- coding: utf-8 -*-

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        MainWindow.setMinimumSize(QSize(600, 300))
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)

        # 背景模糊效果
        self.blurEffect = QGraphicsBlurEffect()
        self.blurEffect.setBlurRadius(15)
        
        self.bgLabel = QLabel(self.centralwidget)
        self.bgLabel.setGraphicsEffect(self.blurEffect)
        self.bgLabel.setStyleSheet("background: rgba(255, 255, 255, 0.9); border-radius: 10px;")
        self.gridLayout.addWidget(self.bgLabel, 0, 0, 4, 4)

        # 标题栏
        self.titleBar = QWidget(self.centralwidget)
        self.titleBar.setFixedHeight(30)
        hbox = QHBoxLayout(self.titleBar)
        hbox.setContentsMargins(0, 0, 0, 0)
        
        self.titleLabel = QLabel("邮件下载管理器")
        self.titleLabel.setStyleSheet("font: bold 14px '微软雅黑'; color: #333;")
        hbox.addWidget(self.titleLabel)
        
        hbox.addStretch()
        
        self.minimizeButton = QPushButton("-")
        self.maximizeButton = QPushButton("□")
        self.closeButton = QPushButton("×")
        
        for btn in [self.minimizeButton, self.maximizeButton, self.closeButton]:
            btn.setFixedSize(24, 24)
            btn.setStyleSheet("""
                QPushButton {
                    border: none; 
                    border-radius: 12px;
                    font: bold 16px;
                }
                QPushButton:hover {
                    background: #ddd;
                }
                #closeButton:hover {
                    background: #ff4444;
                    color: white;
                }
            """)
        
        self.closeButton.setObjectName("closeButton")
        hbox.addWidget(self.minimizeButton)
        hbox.addWidget(self.maximizeButton)
        hbox.addWidget(self.closeButton)
        
        self.gridLayout.addWidget(self.titleBar, 0, 0, 1, 4)

        # 输入区域
        self.formLayout = QFormLayout()
        self.formLayout.setVerticalSpacing(15)
        
        self.mailAddress = QLineEdit()
        self.mailAddress.setPlaceholderText("user@example.com")
        self.imapPassword = QLineEdit()
        self.imapPassword.setEchoMode(QLineEdit.Password)
        
        for widget in [self.mailAddress, self.imapPassword]:
            widget.setMinimumHeight(35)
            widget.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QLineEdit:focus {
                    border-color: #4CAF50;
                }
            """)
        
        self.formLayout.addRow("邮箱地址:", self.mailAddress)
        self.formLayout.addRow("IMAP密码:", self.imapPassword)
        
        # 选项区域
        self.optionsLayout = QHBoxLayout()
        self.checkBox = QCheckBox("记住账号")
        self.checkBox_2 = QCheckBox("记住密码")
        self.downloadHTML = QCheckBox("下载HTML")
        self.seenAfterDownload = QCheckBox("标记已读")
        
        for cb in [self.checkBox, self.checkBox_2, self.downloadHTML, self.seenAfterDownload]:
            cb.setStyleSheet("QCheckBox { color: #666; }")
        
        self.optionsLayout.addWidget(self.checkBox)
        self.optionsLayout.addWidget(self.checkBox_2)
        self.optionsLayout.addWidget(self.downloadHTML)
        self.optionsLayout.addWidget(self.seenAfterDownload)
        
        # 按钮
        self.confirm = QPushButton("开始下载")
        self.confirm.setFixedHeight(40)
        self.confirm.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                border-radius: 5px;
                font: bold 14px;
            }
            QPushButton:hover {
                background: #45a049;
            }
            QPushButton:disabled {
                background: #ccc;
            }
        """)
        
        # 进度条
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                height: 20px;
            }
            QProgressBar::chunk {
                background: #4CAF50;
                border-radius: 4px;
            }
        """)
        
        # 布局整合
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 4)
        self.gridLayout.addLayout(self.optionsLayout, 2, 0, 1, 4)
        self.gridLayout.addWidget(self.confirm, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.progressBar, 3, 1, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        pass  # 翻译内容已直接在代码中设置
