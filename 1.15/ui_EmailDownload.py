# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EmailDownloadIczsJO.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(470, 150)
        MainWindow.setMinimumSize(470, 150)
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mailAddress_Lab = QLabel(self.centralwidget)
        self.mailAddress_Lab.setObjectName(u"mailAddress_Lab")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.mailAddress_Lab.sizePolicy().hasHeightForWidth())
        self.mailAddress_Lab.setSizePolicy(sizePolicy)
        self.mailAddress_Lab.setMinimumSize(QSize(80, 0))
        self.mailAddress_Lab.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.mailAddress_Lab.setFont(font)

        self.horizontalLayout.addWidget(self.mailAddress_Lab)

        self.mailAddress = QTextEdit(self.centralwidget)
        self.mailAddress.setObjectName(u"mailAddress")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(10)
        sizePolicy1.setHeightForWidth(self.mailAddress.sizePolicy().hasHeightForWidth())
        self.mailAddress.setSizePolicy(sizePolicy1)
        self.mailAddress.setMinimumSize(QSize(100, 0))
        self.mailAddress.setMaximumSize(QSize(16777215, 30))
        self.mailAddress.setFont(font)

        self.horizontalLayout.addWidget(self.mailAddress)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy2)
        self.checkBox.setMinimumSize(QSize(100, 0))
        self.checkBox.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox.setFont(font)

        self.horizontalLayout.addWidget(self.checkBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.imapPassword_Lab = QLabel(self.centralwidget)
        self.imapPassword_Lab.setObjectName(u"imapPassword_Lab")
        sizePolicy2.setHeightForWidth(self.imapPassword_Lab.sizePolicy().hasHeightForWidth())
        self.imapPassword_Lab.setSizePolicy(sizePolicy2)
        self.imapPassword_Lab.setMinimumSize(QSize(80, 0))
        self.imapPassword_Lab.setMaximumSize(QSize(16777215, 16777215))
        self.imapPassword_Lab.setFont(font)

        self.horizontalLayout_2.addWidget(self.imapPassword_Lab)

        self.imapPassword = QTextEdit(self.centralwidget)
        self.imapPassword.setObjectName(u"imapPassword")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.imapPassword.sizePolicy().hasHeightForWidth())
        self.imapPassword.setSizePolicy(sizePolicy3)
        self.imapPassword.setMinimumSize(QSize(100, 0))
        self.imapPassword.setMaximumSize(QSize(16777215, 30))
        self.imapPassword.setFont(font)

        self.horizontalLayout_2.addWidget(self.imapPassword)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        sizePolicy2.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy2)
        self.checkBox_2.setMinimumSize(QSize(100, 0))
        self.checkBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox_2.setFont(font)

        self.horizontalLayout_2.addWidget(self.checkBox_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.confirm = QPushButton(self.centralwidget)
        self.confirm.setObjectName(u"confirm")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.confirm.setFont(font1)
        self.confirm.setMouseTracking(False)

        self.horizontalLayout_3.addWidget(self.confirm)

        self.downloadHTML = QCheckBox(self.centralwidget)
        self.downloadHTML.setObjectName(u"downloadHTML")
        self.downloadHTML.setFont(font)

        self.horizontalLayout_3.addWidget(self.downloadHTML)

        self.seenAfterDownload = QCheckBox(self.centralwidget)
        self.seenAfterDownload.setObjectName(u"seenAfterDownload")
        self.seenAfterDownload.setFont(font)

        self.horizontalLayout_3.addWidget(self.seenAfterDownload)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setFont(font)
        self.progressBar.setValue(0)

        self.horizontalLayout_3.addWidget(self.progressBar)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(4, 1)

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"mainWindow", None))
        self.mailAddress_Lab.setText(QCoreApplication.translate("MainWindow", u"\u90ae\u7bb1\u5730\u5740:", None))
        self.mailAddress.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">example@example.com</p></body></html>", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4f\u90ae\u7bb1\u5730\u5740", None))
        self.imapPassword_Lab.setText(QCoreApplication.translate("MainWindow", u"IMAP\u5bc6\u7801:", None))
        self.imapPassword.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Your Password</p></body></html>", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4fIMAP\u5bc6\u7801", None))
        self.confirm.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4", None))
        self.downloadHTML.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7dHTML", None))
        self.seenAfterDownload.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u540e\u6807\u8bb0\u4e3a\u5df2\u8bfb", None))
    # retranslateUi

