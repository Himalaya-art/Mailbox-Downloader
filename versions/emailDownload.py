'''
邮箱下载工具
    GUI界面
    展示已读未读
    下载附件
    下载邮箱正文内容
'''

import email
import PyQt5
import imaplib
import sys
from PyQt5.QtWidgets import *
# import text  # Removed as it cannot be resolved
import datetime
import os
import re
from bs4 import BeautifulSoup
import ui_EmailDownload
from email.parser import BytesParser


class EmailDownload():
    def mail(mailaddress: str, password: str):
        mail = imaplib.IMAP4_SSL('imap.' + mailaddress.split('@')[1])
        mail.login(mailaddress, password)

        mail.select('INBOX')

        sastr, sastr1 = mail.search(None, 'UNSEEN')
        email_list = sastr1[0].split()

        for id in email_list:
            msg = BytesParser().parsebytes(mail.fetch(id, '(RFC822)')[1][0][1])
            valid_subject = re.sub(r'[\\/:*?"<>|]', '', msg['subject'])

            # EML部分
            if msg.is_multipart():
                if part.get_content_type() == 'text/plain':
                    content = part.get_payload(decode=True).decode('utf-8')
                    
                    txt_filepath = os.path.join(valid_subject, valid_subject + '.txt')
                    if not os.path.exists(valid_subject):
                        os.makedirs(valid_subject)
                    with open(txt_filepath, 'w', encoding="utf-8") as f:
                        f.write(content)
                elif part.get_content_type() == 'image/jpeg':
                    jpg_filepath = os.path.join(valid_subject, valid_subject + '.jpg')
                    if not os.path.exists(valid_subject):
                        os.makedirs(valid_subject)
                    with open(jpg_filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                elif part.get_content_type() == 'image/png':
                    png_filepath = os.path.join(valid_subject, valid_subject + '.png')
                    if not os.path.exists(valid_subject):
                        os.makedirs(valid_subject)
                    with open(png_filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                elif part.get_content_type() == 'image/jpg':
                    png_filepath = os.path.join(valid_subject, valid_subject + '.jpg')
                    if not os.path.exists(valid_subject):
                        os.makedirs(valid_subject)
                    with open(png_filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))

            # 附件部分
            for part in msg.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get("Content-Disposition") is None:
                    continue
        
                # 下载附件
                filename = part.get_filename()  # 获取附件的文件名称
                if filename:
                    # 解码文件名
                    decoded_filename = email.header.decode_header(filename)[0][0]
                    if isinstance(decoded_filename, bytes):
                        # 如果解码后的文件名是字节类型，则使用默认字符集进行解码
                        decoded_filename = decoded_filename.decode()
            
                    # 构建文件路径
                    filepath = os.path.join(valid_subject, decoded_filename)
                    if not os.path.isdir(valid_subject):
                        os.mkdir(valid_subject)
            
                    with open(filepath, "wb") as f:
                        # 打开文件以二进制写入模式
                        f.write(part.get_payload(decode=True))


        mail.close()
        mail.logout()

class EmailDownloadUI(QMainWindow, ui_EmailDownload.Ui_MainWindow):
    def __init__(self):
        super(EmailDownloadUI, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.download)
    
    def download(self):
        mailaddress = self.mailAddress.toPlainText()
        password = self.imapPassword.toPlainText()
        EmailDownload.mail(mailaddress, password)
        self.checkBox.setText('下载完成')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = EmailDownloadUI()
    mainWindow.show()
    sys.exit(app.exec_())
    





    


