from netmiko.vyos.vyos_ssh import VyOSSSH
from email.message import EmailMessage
import paramiko
import requests
import smtplib
import os

print('Connecting')
c = VyOSSSH(ip='local IP of the router', username='username', password='password', use_keys=False)
print('Entering Config mode')
c.config_mode()

# Calling what's my ip api
r = requests.get('https://api.ipify.org?format=json')
d = r.json()

for value in d.values():
    print('This is the current IP: '+value)

# Finding the local ip address - Ideally can be either the IP of WAN1 or WAN2
# If ip is ip of WAN1, then delete WAN2 VPN and vise versa. 
print('Finding local address of the current VPN...')
output = c.send_config_set(config_commands='show vpn ipsec site-to-site | grep local-address')

if value in output:
    print("IP not changed")

elif value == 'IP of WAN1':

    # Email notification if ip changes:
    fn = 'Path\\to\\the\\password\\file'
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
    msg['Subject'] = 'IP for xxx has changed'
    msg['From'] = 'ABCD@ABCD.COM'
    msg['To'] = 'XYZ@ABCD.COM'

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login('fABCD@ABCD.COM', password)
    smtpserver.send_message(msg)
    smtpserver.close()

    # As USG controller doesn't seem to support multiple ipsecs so will need to delete the existing ipsec
    # In this case we are going to delete vpn with AWS router 2:
    print('Deleting VPN')
    c.send_config_set(config_commands='delete vpn ipsec site-to-site peer ip of AWS router2')
    c.send_config_set(config_commands='commit')
    c.send_config_set(config_commands='save')
    
    # And now we are going to set up VPN for WAN2'
    print('Building VPN for WAN1')

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

    # Setting up AWS s2s VPN for WAN1
    print('Setting up AWS VPN for WAN1...')

    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 authentication mode pre-shared-secret')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 authentication pre-shared-secret preshaerdkey')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 connection-type initiate')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 default-esp-group ESP-AWS-TEST1')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 ike-group IKE-AWS-TEST1')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 description AWS-TEST-S2S-VPN-1')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 local-address WAN1 IP')
    # tunnel 1
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 1 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 1 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 1 local prefix local subnet_1')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 1 remote prefix remote subnet')
    # tunnel 2
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 2 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 2 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 2 local prefix local subnet_2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router1 tunnel 2 remote prefix remote subnet')

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

    k = paramiko.RSAKey.from_private_key_file("Path\\to\\the\\controller_pem_file")
    cc = paramiko.SSHClient()
    cc.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    cc.connect(hostname='ip of cloud controller', username='controller_username', pkey=k)

    stdin, stdout, stderr = cc.exec_command('sudo cp config1.json /path /to /the /config /file/config.gateway.json')
    cc.close()


elif value == 'IP of WAN2':

    # Email notification phase:
    fn = 'Path\\to\\the\\password\\file'
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
    msg['Subject'] = 'IP for xxx has changed'
    msg['From'] = 'ABCD@ABCD.COM'
    msg['To'] = 'XYZ@ABCD.COM'

    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.login('ABCD@ABCD.COM', password)
    smtpserver.send_message(msg)
    smtpserver.close()

    print('Deleting VPN')
    c.send_config_set(config_commands='delete vpn ipsec site-to-site peer ip of AWS router1')
    c.send_config_set(config_commands='commit')
    c.send_config_set(config_commands='save')

    print('Building VPN for wan2')
    
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
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 authentication mode pre-shared-secret presharedkey')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 authentication pre-shared-secret ')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 connection-type initiate')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 default-esp-group ESP-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 ike-group IKE-AWS-TEST2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 description AWS-TEST2-S2S-VPN')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 local-address ip of wan2')
    # tunnel 1
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 1 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 1 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 1 local prefix local subnet')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 1 remote prefix remote subnet')
    # tunnel 2
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 2 allow-nat-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 2 allow-public-networks disable')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 2 local prefix local subnet 2')
    c.send_config_set(config_commands='set vpn ipsec site-to-site peer ip of AWS router2 tunnel 2 remote prefix remote subnet')

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

    k = paramiko.RSAKey.from_private_key_file("Path\\to\\the\\controller_pem_file")
    cc = paramiko.SSHClient()
    cc.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    cc.connect(hostname='ip of cloud controller', username='ubuntu', pkey=k)
    stdin, stdout, stderr = cc.exec_command('sudo cp config2.json /path /to /the /config /file/config.gateway.json')
    cc.close()
