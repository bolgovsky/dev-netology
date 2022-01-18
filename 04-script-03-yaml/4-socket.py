import socket
import time
import json
from builtins import set

import yaml

dns_ip = {
    "drive.google.com": '',
    'mail.google.com': '',
    'google.com': ''
    }
separator = '--------------'
print("First resolving DNS-IP to set default values: ")
for dns in dns_ip:
    resolve_ip=socket.gethostbyname(dns)
    dns_ip[dns] = resolve_ip
for dns , ip in dns_ip.items():
    print(dns+' - '+ip)
with open('dns_ip.yaml', 'w') as ym1:
    ym1.write(yaml.dump(dns_ip))
print("write to dns_ip.yaml: \n"+yaml.dump(dns_ip))
with open('dns_ip.json', 'w') as js1:
    js1.write(json.dumps(dns_ip))
print("write to dns_ip.json: \n"+json.dumps(dns_ip))
print(separator)
while True:
    for dns, current_ip in dns_ip.items():
        check_ip = socket.gethostbyname(dns)
        time.sleep(1)
        if check_ip != current_ip:
            dns_ip[dns] = check_ip
            print(f'[ERROR] {dns} IP mismatch: {current_ip} New IP: {check_ip} \n')
            with open('dns_ip.yaml', 'w') as ym1:
                ym1.write(yaml.dump(dns_ip))
            print("yaml-file: \n" + yaml.dump(dns_ip))
            with open('dns_ip.json', 'w') as js1:
                js1.write(json.dumps(dns_ip))
            print("json-file: \n" + json.dumps(dns_ip))
            print(separator)
        else:
            print(f'{dns} - {current_ip}')