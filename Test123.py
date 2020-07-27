from netmiko.vyos.vyos_ssh import VyOSSSH
import requests

print('Connecting')
#c=VyOSSSH(ip='54.66.164.57', username='vyos', key_file="c:\\scripts\\private.pem", use_keys=True)

# IT Demon with 4G
c=VyOSSSH(ip='192.168.168.1', username='xyli', password='T7XOHict', use_keys=False)
print('Entering Config mode')
c.config_mode()
c.send_config_set(config_commands='configure')
print(c.send_config_set(config_commands='set vpn ipsec site-to-site peer 13.54.103.194 local-address 123.209.226.173'))