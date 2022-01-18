import socket
import time

dns_ip = {
    "drive.google.com": '',
    'mail.google.com': '',
    'google.com': ''
    }

print("First resolving DNS-IP to set default values: ")
for dns in dns_ip:
    resolve_ip=socket.gethostbyname(dns)
    dns_ip[dns] = resolve_ip
for dns , ip in dns_ip.items():
    print(dns+' - '+ip)
print('\n')

while True:
    for dns, current_ip in dns_ip.items():
        check_ip = socket.gethostbyname(dns)
        time.sleep(1)
        if check_ip != current_ip:
            dns_ip[dns] = check_ip
            print(f'[ERROR] {dns} IP mismatch: {current_ip} New IP: {check_ip}')
        else:
            print(f'{dns} - {current_ip}')