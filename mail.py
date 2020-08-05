import smtplib
from email.mime.text import MIMEText

class Mail(object):
    """docstring for Mail"""
    def __init__(self, smtpserver, username, password):
        super(Mail, self).__init__()
        self.server = smtplib.SMTP(smtpserver)
        self.username = username
        self.password = password

    def send(self, me, you, subject, message):
        self.server.login(self.username, self.password)
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you
        self.server.sendmail(me, [you], msg.as_string())
        self.server.quit()

# mail = Mail(smtp, u, p)
# mail.send(Me, You, "hello run", "ok and test")