import smtplib
from email.message import EmailMessage
import os

fn = 'c:\\Users\\eddie.zhang\\Desktop\\pass(2).txt'
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
msg['From'] = 'eddie.zhang@vet.partners'
msg['To'] = 'yuan.li@vet.partners', 'eddie.zhang@vet.partners'

smtpserver.ehlo()
smtpserver.starttls()
smtpserver.login('eddie.zhang@vet.partners', password)
smtpserver.send_message(msg)
smtpserver.close()
