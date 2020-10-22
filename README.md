# AWS-VPN-remains-connected-when-WAN-IP-changes
Automatically create an s2s vpn between an on-prem environment and AWS when wan1 fails over to wan2 and vice versa. 
Updated on 23/10 - User responded that VPN dropped out after a restart - this is because the configure.gateway.json file for this particular site wasn't updated accordingly in cloud controller. 
So I updated my code so that it automatically downloads the configuration file for this site/router and makes it a JSON file then uploads to cloud controller with name configure.gateway.json.
