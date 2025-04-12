/********************************************************************************
** Form generated from reading UI file 'EmailDownloadcccQWL.ui'
**
** Created by: Qt User Interface Compiler version 5.15.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef EMAILDOWNLOADCCCQWL_H
#define EMAILDOWNLOADCCCQWL_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QLabel>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QGridLayout *gridLayout;
    QTextEdit *mailAddress;
    QTextEdit *imapPassword;
    QPushButton *confirm;
    QProgressBar *progressBar;
    QCheckBox *checkBox;
    QCheckBox *checkBox_2;
    QLabel *imapPassword_Lab;
    QLabel *mailAddress_Lab;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(538, 212);
        MainWindow->setMinimumSize(QSize(538, 212));
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName(QString::fromUtf8("centralwidget"));
        gridLayout = new QGridLayout(centralwidget);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        mailAddress = new QTextEdit(centralwidget);
        mailAddress->setObjectName(QString::fromUtf8("mailAddress"));
        QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(mailAddress->sizePolicy().hasHeightForWidth());
        mailAddress->setSizePolicy(sizePolicy);
        QFont font;
        font.setFamily(QString::fromUtf8("\345\276\256\350\275\257\351\233\205\351\273\221"));
        mailAddress->setFont(font);

        gridLayout->addWidget(mailAddress, 0, 1, 2, 2);

        imapPassword = new QTextEdit(centralwidget);
        imapPassword->setObjectName(QString::fromUtf8("imapPassword"));
        sizePolicy.setHeightForWidth(imapPassword->sizePolicy().hasHeightForWidth());
        imapPassword->setSizePolicy(sizePolicy);
        imapPassword->setFont(font);

        gridLayout->addWidget(imapPassword, 2, 1, 2, 2);

        confirm = new QPushButton(centralwidget);
        confirm->setObjectName(QString::fromUtf8("confirm"));
        confirm->setFont(font);

        gridLayout->addWidget(confirm, 4, 0, 1, 2);

        progressBar = new QProgressBar(centralwidget);
        progressBar->setObjectName(QString::fromUtf8("progressBar"));
        progressBar->setFont(font);
        progressBar->setValue(12);

        gridLayout->addWidget(progressBar, 4, 2, 1, 2);

        checkBox = new QCheckBox(centralwidget);
        checkBox->setObjectName(QString::fromUtf8("checkBox"));
        checkBox->setMaximumSize(QSize(16777215, 16777215));
        checkBox->setFont(font);

        gridLayout->addWidget(checkBox, 0, 3, 2, 1);

        checkBox_2 = new QCheckBox(centralwidget);
        checkBox_2->setObjectName(QString::fromUtf8("checkBox_2"));
        checkBox_2->setMaximumSize(QSize(16777215, 16777215));
        checkBox_2->setFont(font);

        gridLayout->addWidget(checkBox_2, 2, 3, 2, 1);

        imapPassword_Lab = new QLabel(centralwidget);
        imapPassword_Lab->setObjectName(QString::fromUtf8("imapPassword_Lab"));
        imapPassword_Lab->setMaximumSize(QSize(16777215, 16777215));
        imapPassword_Lab->setFont(font);

        gridLayout->addWidget(imapPassword_Lab, 2, 0, 2, 1);

        mailAddress_Lab = new QLabel(centralwidget);
        mailAddress_Lab->setObjectName(QString::fromUtf8("mailAddress_Lab"));
        mailAddress_Lab->setMaximumSize(QSize(16777215, 16777215));
        mailAddress_Lab->setFont(font);

        gridLayout->addWidget(mailAddress_Lab, 0, 0, 2, 1);

        MainWindow->setCentralWidget(centralwidget);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName(QString::fromUtf8("statusbar"));
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        mailAddress->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\345\276\256\350\275\257\351\233\205\351\273\221'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">example@example.com</p></body></html>", nullptr));
        imapPassword->setHtml(QCoreApplication::translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'\345\276\256\350\275\257\351\233\205\351\273\221'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Your Password</p></body></html>", nullptr));
        confirm->setText(QCoreApplication::translate("MainWindow", "\347\241\256\350\256\244", nullptr));
        checkBox->setText(QCoreApplication::translate("MainWindow", "\350\256\260\344\275\217\351\202\256\347\256\261\345\234\260\345\235\200", nullptr));
        checkBox_2->setText(QCoreApplication::translate("MainWindow", "\350\256\260\344\275\217IMAP\345\257\206\347\240\201", nullptr));
        imapPassword_Lab->setText(QCoreApplication::translate("MainWindow", "IMAP\345\257\206\347\240\201\357\274\232", nullptr));
        mailAddress_Lab->setText(QCoreApplication::translate("MainWindow", "\351\202\256\347\256\261\345\234\260\345\235\200:", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // EMAILDOWNLOADCCCQWL_H
