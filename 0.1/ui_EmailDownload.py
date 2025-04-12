# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EmailDownloadmkoyBH.ui'
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
        MainWindow.resize(700, 220)
        MainWindow.setMinimumSize(700, 220)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.mailAddress = QTextEdit(self.centralwidget)
        self.mailAddress.setObjectName(u"mailAddress")
        font = QFont()
        font.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        self.mailAddress.setFont(font)

        self.gridLayout.addWidget(self.mailAddress, 0, 1, 2, 4)

        self.imapPassword = QTextEdit(self.centralwidget)
        self.imapPassword.setObjectName(u"imapPassword")
        self.imapPassword.setFont(font)

        self.gridLayout.addWidget(self.imapPassword, 2, 1, 2, 4)

        self.confirm = QPushButton(self.centralwidget)
        self.confirm.setObjectName(u"confirm")
        font1 = QFont()
        font1.setFamily(u"\u5fae\u8f6f\u96c5\u9ed1")
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.confirm.setFont(font1)
        self.confirm.setMouseTracking(False)

        self.gridLayout.addWidget(self.confirm, 4, 0, 1, 2)

        self.downloadHTML = QCheckBox(self.centralwidget)
        self.downloadHTML.setObjectName(u"downloadHTML")
        self.downloadHTML.setFont(font)

        self.gridLayout.addWidget(self.downloadHTML, 4, 2, 1, 1)

        self.seenAfterDownload = QCheckBox(self.centralwidget)
        self.seenAfterDownload.setObjectName(u"seenAfterDownload")
        self.seenAfterDownload.setFont(font)

        self.gridLayout.addWidget(self.seenAfterDownload, 4, 3, 1, 1)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setFont(font)
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 4, 4, 1, 2)

        self.mailAddress_Lab = QLabel(self.centralwidget)
        self.mailAddress_Lab.setObjectName(u"mailAddress_Lab")
        self.mailAddress_Lab.setMaximumSize(QSize(16777215, 16777215))
        self.mailAddress_Lab.setFont(font)

        self.gridLayout.addWidget(self.mailAddress_Lab, 0, 0, 2, 1)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox.setFont(font)

        self.gridLayout.addWidget(self.checkBox, 0, 5, 2, 1)

        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.checkBox_2.setFont(font)

        self.gridLayout.addWidget(self.checkBox_2, 2, 5, 2, 1)

        self.imapPassword_Lab = QLabel(self.centralwidget)
        self.imapPassword_Lab.setObjectName(u"imapPassword_Lab")
        self.imapPassword_Lab.setMaximumSize(QSize(16777215, 16777215))
        self.imapPassword_Lab.setFont(font)

        self.gridLayout.addWidget(self.imapPassword_Lab, 2, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.mailAddress.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">example@example.com</p></body></html>", None))
        self.imapPassword.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\u5fae\u8f6f\u96c5\u9ed1'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Your Password</p></body></html>", None))
        self.confirm.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4", None))
        self.downloadHTML.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7dHTML", None))
        self.seenAfterDownload.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u540e\u6807\u8bb0\u4e3a\u5df2\u8bfb", None))
        self.mailAddress_Lab.setText(QCoreApplication.translate("MainWindow", u"\u90ae\u7bb1\u5730\u5740:", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4f\u90ae\u7bb1\u5730\u5740", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u4f4fIMAP\u5bc6\u7801", None))
        self.imapPassword_Lab.setText(QCoreApplication.translate("MainWindow", u"IMAP\u5bc6\u7801\uff1a", None))
    # retranslateUi

