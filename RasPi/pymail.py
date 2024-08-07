# pimail.py
# envoi de mail en python
# 2016-06-13	PV

import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders


def send_mail(send_from, send_to, subject, text, files=[], server="localhost", port=25, username='', password='', isTls=True):
	msg = MIMEMultipart()
	msg['From'] = send_from
	msg['To'] = COMMASPACE.join(send_to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach(MIMEText(text))

	for f in files:
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(f, "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)))
		msg.attach(part)

	smtp = smtplib.SMTP(server, port)
	if isTls: smtp.starttls()
	if len(username)>0: smtp.login(username, password)
	smtp.sendmail(send_from, send_to, msg.as_string())
	smtp.quit()



email_from = "pierre.violent@gmail.com"
email_to = "frenchbear38@gmail.com"

source = "/home/pi/Python/pymail.py"
send_mail(email_from, [email_to], "Test message #3", "From raspberry Pi gluon3, in Python", [source], "smtp.gmail.com", "587", "pierre.violent", "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", True)


