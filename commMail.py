#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2016 WShuai, Inc.
# All Rights Reserved.

# @author: WShuai, WShuai, Inc.

'''
Send Mail
'''

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate
from email import encoders

class MailHandler(object):
    def __init__(self, mail_server_name, mail_server_port, mail_server_user, mail_server_pass, mail_outbox):
        self.mail_server_name = mail_server_name
        self.mail_server_port = mail_server_port
        self.mail_server_user = mail_server_user
        self.mail_server_pass = mail_server_pass
        self.mail_outbox = mail_outbox
        self.mail_inbox = None
        return

    def send_mail(self, mail_inbox, mail_subject, mail_body, files=[]):
        self.mail_inbox = mail_inbox.split(',')
        msg = MIMEMultipart()
        msg['From'] = self.mail_outbox
        msg['Subject'] = mail_subject
        msg['To'] = COMMASPACE.join(self.mail_inbox)
        msg['Date'] = formatdate(localtime=True)
        msg.attach(MIMEText(mail_body))

        for f in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(f, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
            msg.attach(part)

        smtp = smtplib.SMTP(self.mail_server_name, self.mail_server_port)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(self.mail_server_user, self.mail_server_pass)
        smtp.sendmail(self.mail_outbox, self.mail_inbox, msg.as_string())
        smtp.close()
        return

'''
例子
'''

import sys
if __name__ == '__main__':
    mail_handler = MailHandler(
        'smtp.yeah.net',
        25,
        'herohub@yeah.net',
        'XXXXXXXXXXXXX',
        'herohub@yeah.net'
    )
    mail_handler.send_mail('553704997@qq.com', 'test', 'this is test', ['./test.log'])
    sys.exit(0)
