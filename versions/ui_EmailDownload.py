# ui_EmailDownload.py
from PySide2.QtCore import Qt, QSize, QMetaObject, QCoreApplication
from PySide2.QtGui import QFont, QPixmap, QColor
from PySide2.QtWidgets import (
    QMainWindow, QWidget, QLabel, QGridLayout, QHBoxLayout,
    QPushButton, QLineEdit, QCheckBox, QProgressBar, QTextEdit,
    QSizePolicy, QSpacerItem
)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 680)  # 调整初始窗口尺寸
        MainWindow.setMinimumSize(QSize(860, 560))
        MainWindow.setWindowFlags(Qt.FramelessWindowHint)
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)

        # 主容器（增强阴影效果）
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-image: url(background.png);
                background-size: cover;
                border-radius: 16px;
                border: 1px solid rgba(255,255,255,0.35);
                box-shadow: 0 12px 32px rgba(0,0,0,0.25);
            }
        """)
        
        # 主布局（优化边距）
        self.mainLayout = QGridLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(1, 1, 1, 1)
        self.mainLayout.setSpacing(0)

        # 现代标题栏（毛玻璃效果）
        self.titleBar = QWidget()
        self.titleBar.setFixedHeight(52)
        self.titleBar.setStyleSheet("""
            background-color: rgba(40,40,40,0.95);
            border-radius: 16px 16px 0 0;
        """)
        
        # 标题栏布局（优化间距）
        self.titleLayout = QHBoxLayout(self.titleBar)
        self.titleLayout.setContentsMargins(20, 0, 20, 0)
        self.titleLayout.setSpacing(25)

        # 增强图标显示
        self.iconLabel = QLabel()
        self.iconLabel.setPixmap(QPixmap("icon.png").scaled(40, 40, 
            Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.titleLabel = QLabel("智能邮件下载器")
        self.titleLabel.setStyleSheet("""
            QLabel {
                color: white;
                font: bold 22px 'Microsoft YaHei';
                padding-left: 12px;
                letter-spacing: 1px;
            }
        """)

        # 窗口控制按钮（增强交互反馈）
        self.winButtons = QHBoxLayout()
        self.winButtons.setSpacing(15)
        self.minimizeButton = self._create_win_button("—", "#606060", hover_scale=1.1)
        self.maximizeButton = self._create_win_button("□", "#606060", hover_scale=1.1) 
        self.closeButton = self._create_win_button("×", "#ff5555", hover_scale=1.2)

        # 组装标题栏
        self.titleLayout.addWidget(self.iconLabel)
        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.addStretch()
        self.titleLayout.addLayout(self.winButtons)

        # 内容区域（优化透明度）
        self.contentWidget = QWidget()
        self.contentWidget.setStyleSheet("""
            background-color: rgba(255,255,255,0.88);
            border-radius: 0 0 16px 16px;
        """)
        
        # 增强内容布局
        self.contentLayout = QGridLayout(self.contentWidget)
        self.contentLayout.setContentsMargins(35, 35, 35, 35)
        self.contentLayout.setVerticalSpacing(25)
        self.contentLayout.setHorizontalSpacing(30)

        # 构建增强表单
        self._create_enhanced_form()
        
        # 日志区域（优化显示效果）
        self.logArea = QTextEdit()
        self.logArea.setStyleSheet("""
            QTextEdit {
                background: rgba(255,255,255,0.92);
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 15px;
                font: 13px 'Consolas';
                color: #444;
            }
            QScrollBar:vertical {
                width: 10px;
                background: rgba(240,240,240,0.8);
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 30px;
            }
        """)
        self.logArea.setMinimumHeight(180)
        
        # 增强进度条设计
        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(28)
        self.progressBar.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.95);
                border: 2px solid #e0e0e0;
                border-radius: 14px;
                text-align: center;
                font: 14px 'Microsoft YaHei';
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #45a049
                );
                border-radius: 12px;
                border: 1px solid #388E3C;
            }
        """)

        # 增强操作按钮（添加点击事件绑定）
        self.confirm = QPushButton("🚀 开始下载")
        self.confirm.setFixedSize(160, 48)
        self.confirm.clicked.connect(MainWindow.start_download)  # 添加事件绑定
        self.confirm.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 24px;
                font: bold 18px 'Microsoft YaHei';
                min-width: 140px;
                padding: 0 20px;
                transition: all 0.3s ease;
            }
            QPushButton:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                transform: scale(0.95);
            }
            QPushButton:disabled {
                background-color: #a0a0a0;
            }
        """)

        # 最终布局组合
        self.contentLayout.addWidget(self.logArea, 3, 0, 1, 4)
        self.contentLayout.addWidget(self.progressBar, 4, 0, 1, 3)
        self.contentLayout.addWidget(self.confirm, 4, 3)

        self.mainLayout.addWidget(self.titleBar, 0, 0)
        self.mainLayout.addWidget(self.contentWidget, 1, 0)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def _create_win_button(self, text, bg_color, hover_scale=1.0):
        """创建现代化窗口控制按钮"""
        button = QPushButton(text)
        button.setFixedSize(40, 40)
        button.setStyleSheet(f"""
            QPushButton {{
                color: white;
                border: none;
                border-radius: 20px;
                font: bold 24px 'Arial';
                background: {bg_color};
                transition: all 0.2s ease;
            }}
            QPushButton:hover {{
                transform: scale({hover_scale});
                opacity: 0.9;
            }}
        """)
        return button

    def _create_input_field(self, placeholder, is_password=False, icon=None):
        """创建带图标的输入框"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # if icon:  # 暂时注释图标相关代码
        #     icon_label = QLabel()
        #     icon_label.setPixmap(QPixmap(icon).scaled(24, 24))
        #     layout.addWidget(icon_label)
        
        lineedit = QLineEdit()
        lineedit.setObjectName("emailInput" if "邮箱地址" in placeholder else "passwordInput")
        lineedit.setPlaceholderText(placeholder)
        lineedit.setMinimumHeight(44)
        lineedit.setStyleSheet("""
            QLineEdit {
                background: rgba(255,255,255,0.95);
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 0 15px;
                font: 16px 'Microsoft YaHei';
                selection-background-color: #4CAF50;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50;
                background: white;
            }
        """)
        if is_password:
            lineedit.setEchoMode(QLineEdit.Password)
        
        layout.addWidget(lineedit)  # 修复：添加正确的 lineedit 控件
        return container

    def _create_enhanced_form(self):
        """创建增强型输入表单"""
        # 邮箱地址输入
        self.mailAddress_Lab = QLabel("电子邮箱：")
        self.mailAddress_Lab.setStyleSheet("font: 16px 'Microsoft YaHei'; color: #333;")
        self.mailAddress = self._create_input_field("请输入邮箱地址", icon="mail_icon.png")
        
        # 密码输入
        self.imapPassword_Lab = QLabel("安全密码：")
        self.imapPassword_Lab.setStyleSheet("font: 16px 'Microsoft YaHei'; color: #333;")
        self.imapPassword = self._create_input_field("请输入IMAP密码", is_password=True, icon="lock_icon.png")
        
        # 增强复选框
        self.checkBox = self._create_enhanced_checkbox("记住邮箱地址")
        self.checkBox_2 = self._create_enhanced_checkbox("记住密码")
        self.downloadHTML = self._create_enhanced_checkbox("下载HTML内容", checked=True)
        self.seenAfterDownload = self._create_enhanced_checkbox("标记已读邮件")

        # 表单布局（优化响应式）
        self.contentLayout.addWidget(self.mailAddress_Lab, 0, 0)
        self.contentLayout.addWidget(self.mailAddress, 0, 1)
        self.contentLayout.addWidget(self.checkBox, 0, 2)
        self.contentLayout.addWidget(self.downloadHTML, 0, 3)
        
        self.contentLayout.addWidget(self.imapPassword_Lab, 1, 0)
        self.contentLayout.addWidget(self.imapPassword, 1, 1)
        self.contentLayout.addWidget(self.checkBox_2, 1, 2)
        self.contentLayout.addWidget(self.seenAfterDownload, 1, 3)

    def _create_enhanced_checkbox(self, text, checked=False):
        """创建增强型复选框"""
        checkbox = QCheckBox(text)
        checkbox.setChecked(checked)
        checkbox.setStyleSheet("""
            QCheckBox {
                font: 16px 'Microsoft YaHei';
                color: #333;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 24px;
                height: 24px;
            }
            QCheckBox::indicator:unchecked {
                background: #e0e0e0;
                border: 2px solid #c0c0c0;
                border-radius: 4px;
            }
            QCheckBox::indicator:checked {
                background: #4CAF50;
                border: 2px solid #388E3C;
                border-radius: 4px;
            }
        """)
        return checkbox
    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "智能邮件下载器"))
        self.titleLabel.setText(_translate("MainWindow", "智能邮件下载器"))
        self.mailAddress_Lab.setText(_translate("MainWindow", "电子邮箱："))
        self.imapPassword_Lab.setText(_translate("MainWindow", "安全密码："))
        self.checkBox.setText(_translate("MainWindow", "记住邮箱地址"))
        self.checkBox_2.setText(_translate("MainWindow", "记住密码"))
        self.downloadHTML.setText(_translate("MainWindow", "下载HTML内容"))
        self.seenAfterDownload.setText(_translate("MainWindow", "标记已读邮件"))
        self.confirm.setText(_translate("MainWindow", "🚀 开始下载"))
