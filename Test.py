import os
fn = 'c:\\Users\\eddie.zhang\\Desktop\\pass(2).txt'
p = os.popen('attrib +h' + fn)
t = p.read()
p.close()


# import paramiko
# k = paramiko.RSAKey.from_private_key_file("c:\\Users\\eddie.zhang\\Desktop\\UniFiController.pem")
# c = paramiko.SSHClient()
# c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# c.connect(hostname='52.62.211.89', username='ubuntu', pkey=k)
#
# stdin, stdout, stderr = c.exec_command('sudo cp config2.json /usr/lib/unifi/data/sites/irbao34v/config.gateway.json')


# commands = ['df -H', 'sudo cp config2.json usr/lib/unifi/data/sites/irbao34v/config.gateway.json', 'ls /usr/lib/unifi/data/sites/irbao34v -la']
#
# for item in commands:
#     stdin, stdout, stderr = c.exec_command(item)
#     result = stdout.read()
#     print(len(result))
#     print(result.decode())