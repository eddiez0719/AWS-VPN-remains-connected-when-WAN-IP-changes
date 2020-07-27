from netmiko.vyos.vyos_ssh import VyOSSSH
from email.message import EmailMessage
import paramiko
import requests
import smtplib
import os


k = paramiko.RSAKey.from_private_key_file("c:\\Users\\eddie.zhang\\Desktop\\UniFiController.pem")
cc = paramiko.SSHClient()
cc.set_missing_host_key_policy(paramiko.AutoAddPolicy())

cc.connect(hostname='52.62.211.89', username='ubuntu', pkey=k)
stdin, stdout, stderr = cc.exec_command('sudo cp config1.json /usr/lib/unifi/data/sites/irbao34v/config.gateway.json')
cc.close()