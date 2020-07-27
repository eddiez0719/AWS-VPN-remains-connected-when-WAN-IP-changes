import smtplib
from email.message import EmailMessage
import os

fn = 'c:\\PATH\\TO THE PASSWORD\\FILE'
p = os.popen('attrib +h' + fn)
t = p.read()
p.close()

f = open(fn, 'r')
lines = f.readlines()
password = lines[0]
f.close()

smtpsvr = 'smtp.office365.com'
smtpserver = smtplib.SMTP(smtpsvr, 587)

msg = EmailMessage()
msg['Subject'] = 'IP has changed'
msg['From'] = 'ABCD@ABCD.COM'
msg['To'] = 'XYZ@ABCD.COM

smtpserver.ehlo()
smtpserver.starttls()
smtpserver.login('ABCD@ABCD.COM', password)
smtpserver.send_message(msg)
smtpserver.close()
