from netmiko.vyos.vyos_ssh import VyOSSSH
from email.message import EmailMessage
import paramiko
import requests
import smtplib
import os

print('Connecting')
#c=VyOSSSH(ip='54.66.164.57', username='vyos', key_file="c:\\scripts\\private.pem", use_keys=True)

# IT Demon with 4G
#c = VyOSSSH(ip='192.168.168.1', username='xyli', password='T7XOHict', use_keys=False)
c = VyOSSSH(ip='10.2.29.1', username='SteveVetUnifi', password='rPRRrqr0dyBV0yrO7', use_keys=False)
print('Entering Config mode')
c.config_mode()
#c.send_config_set(config_commands='configure')

r = requests.get('https://api.ipify.org?format=json')
d = r.json()


for value in d.values():
    print('This is the current IP: '+value)

# Finding local address:
print('Finding local address of the current VPN...')

# Either can be 123.209.79.139 (WAN1) or 123.209.87.142 (WAN2)
# Either can be 203.194.45.6 (WAN1) or 14.200.216.194 (WAN2)
output = c.send_config_set(config_commands='show vpn ipsec site-to-site | grep local-address')


if value in output:
    print("IP not changed")

elif value == '203.194.45.6':

    # Email notification phase:
    fn = 'c:\\Users\\xezhang\\Desktop\\pass(2).txt'
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
    msg['Subject'] = 'IP for SVES has changed'
    msg['From'] = 'frank@vet.partners'
    msg['To'] = 'yuan.li@vet.partners', 'eddie.zhang@vet.partners'

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login('frank@vet.partners', password)
    smtpserver.send_message(msg)
    smtpserver.close()

    # VPN Processing phase:
    print('Deleting VPN')
    # c.send_config_set(config_commands='delete vpn ipsec site-to-site peer 13.55.5.211')
    c.send_config_set(config_commands='delete vpn ipsec site-to-site peer 3.105.152.145')
    c.send_config_set(config_commands='commit')
    c.send_config_set(config_commands='save')
    #print('Building VPN for 123.209.79.173')
    print('Building VPN for 203.194.45.6')


    print('Configuring ESP Groups....')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST compression enable')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST lifetime 28800')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST mode tunnel')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST pfs enable')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST proposal 1')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST proposal 1 encryption aes256')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST proposal 1 hash sha1')

    print('Configuring IKE Groups...')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST dead-peer-detection')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST dead-peer-detection action restart')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST dead-peer-detection interval 30')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST dead-peer-detection timeout 120')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST key-exchange ikev1')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST lifetime 28800')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST proposal 1')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST proposal 1 encryption aes256')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST proposal 1 hash sha1')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST proposal 1 dh-group 2')

    print('Configuring ipsec interfaces...')
    c.send_config_set(config_commands='set vpn ipsec ipsec-interfaces interface eth0')
    c.send_config_set(config_commands='set vpn ipsec ipsec-interfaces interface eth2')

    print('Configuring allowed networks behind NAT...')
    c.send_config_set(config_commands='set vpn ipsec nat-networks allowed-network 0.0.0.0/0')

    print('Configuring site to site VPN...')
    c.send_config_set(config_commands='set vpn ipsec auto-firewall-nat-exclude enable')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST compression disable')

    # Building up the AWS VPN for WAN2
    print('Building up the AWS VPN for WAN1...')
    #c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.163.215')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 authentication mode pre-shared-secret')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 authentication pre-shared-secret nn23sdk6')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 connection-type initiate')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 default-esp-group ESP-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 ike-group IKE-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 description AWS-TEST-S2S-VPN-2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 local-address 203.194.45.6')
    # tunnel 1
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 1 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 1 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 1 local prefix 10.2.29.0/24')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 1 remote prefix 172.31.0.0/16')
    # tunnel 2
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 2 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 2 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 2 local prefix 192.168.1.0/24')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.124.84 tunnel 2 remote prefix 172.31.0.0/16')

    print('Saving configuration...')
    c.send_config_set(config_commands='commit')
    c.send_config_set(config_commands='save')
    output1 = c.send_config_set(config_commands='show vpn')
    print(output1)

    # Export the current JSON configuration file
    c.send_config_set(config_commands='mca-ctrl -t dump-cfg > config1.txt')
    c.exit_config_mode()
    c.disconnect()

    # Download with Powershell scripts

    # SSH into Cloud Controller and modify the JSON configuration file - hasn't tested in bulk run

    k = paramiko.RSAKey.from_private_key_file("c:\\Users\\xezhang\\Desktop\\UniFiController.pem")
    cc = paramiko.SSHClient()
    cc.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    cc.connect(hostname='52.62.211.89', username='ubuntu', pkey=k)

    stdin, stdout, stderr = cc.exec_command('sudo cp config1.json /usr/lib/unifi/data/sites/irbao34v/config.gateway.json')
    cc.close()


elif value == '14.200.216.194':

    # Email notification phase:
    fn = 'c:\\Users\\xezhang\\Desktop\\pass(2).txt'
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
    msg['Subject'] = 'IP for SVES has changed'
    msg['From'] = 'frank@vet.partners'
    msg['To'] = 'yuan.li@vet.partners', 'eddie.zhang@vet.partners'

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login('frank@vet.partners', password)
    smtpserver.send_message(msg)
    smtpserver.close()

    # VPN Processing phase:
    print('Deleting VPN')
    c.send_config_set(config_commands='delete vpn ipsec site-to-site peer 13.54.124.84')
    c.send_config_set(config_commands='commit')
    c.send_config_set(config_commands='save')
    print('Building VPN for 14.200.216.194')
    print('Configuring ESP Groups....')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 compression enable')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 lifetime 28800')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 mode tunnel')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 pfs enable')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 proposal 1')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 proposal 1 encryption aes256')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 proposal 1 hash sha1')

    print('Configuring IKE Groups...')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 dead-peer-detection')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 dead-peer-detection action restart')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 dead-peer-detection interval 30')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 dead-peer-detection timeout 120')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 key-exchange ikev1')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 lifetime 28800')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 proposal 1')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 proposal 1 encryption aes256')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 proposal 1 hash sha1')
    c.send_config_set(config_commands='set vpn ipsec ike-group IKE-AWS-TEST2 proposal 1 dh-group 2')

    print('Configuring ipsec interfaces...')
    c.send_config_set(config_commands='set vpn ipsec ipsec-interfaces interface eth0')
    c.send_config_set(config_commands='set vpn ipsec ipsec-interfaces interface eth2')

    print('Configuring allowed networks behind NAT...')
    c.send_config_set(config_commands='set vpn ipsec nat-networks allowed-network 0.0.0.0/0')

    print('Configuring site to site VPN...')
    c.send_config_set(config_commands='set vpn ipsec auto-firewall-nat-exclude enable')
    c.send_config_set(config_commands='set vpn ipsec esp-group ESP-AWS-TEST2 compression disable')

    # Building up the AWS VPN for WAN2
    print('Building up the AWS VPN for WAN2...')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 authentication mode pre-shared-secret nn23sdk6')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 authentication pre-shared-secret ')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 connection-type initiate')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 default-esp-group ESP-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 ike-group IKE-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 description AWS-TEST2-S2S-VPN')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 local-address 14.200.216.194')
    # tunnel 1
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 1 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 1 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 1 local prefix 10.2.29.0/24')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 1 remote prefix 172.31.0.0/16')
    # tunnel 2
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 2 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 2 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 2 local prefix 192.168.1.0/24')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer 3.105.152.145 tunnel 2 remote prefix 172.31.0.0/16')

    print('Saving configuration...')
    c.send_config_set(config_commands='commit')
    c.send_config_set(config_commands='save')
    output2 = c.send_config_set(config_commands='show vpn')
    print(output2)

    # Export the current JSON configuration file
    c.send_config_set(config_commands='mca-ctrl -t dump-cfg > config2.txt')
    c.exit_config_mode()
    c.disconnect()

    # Download with Powershell scripts
    # SSH into Cloud Controller and modify the JSON configuration file - hasn't tested in bulk run

    k = paramiko.RSAKey.from_private_key_file("c:\\Users\\xezhang\\Desktop\\UniFiController.pem")
    cc = paramiko.SSHClient()
    cc.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    cc.connect(hostname='52.62.211.89', username='ubuntu', pkey=k)
    stdin, stdout, stderr = cc.exec_command('sudo cp config2.json /usr/lib/unifi/data/sites/irbao34v/config.gateway.json')
    cc.close()

    






