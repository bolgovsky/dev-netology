# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:   

Нужно найти и исправить все ошибки, которые допускает наш сервис

Ответ: нужно обязательно указывать ключ в кавычках, а если значение однозначно не интерпретируется как допустимый тип, то и значене в кавычки:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```


## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
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
            print(separator)
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
```

### Вывод скрипта при запуске при тестировании:
```
C:\Users\Денис\AppData\Local\Programs\Python\Python39\python.exe C:/Users/Денис/PycharmProjects/dev-netology/04-script-03-yaml/4-socket.py
First resolving DNS-IP to set default values: 
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 74.125.205.100
write to dns_ip.yaml: 
drive.google.com: 173.194.222.194
google.com: 74.125.205.100
mail.google.com: 173.194.222.18

write to dns_ip.json: 
{"drive.google.com": "173.194.222.194", "mail.google.com": "173.194.222.18", "google.com": "74.125.205.100"}
--------------
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 74.125.205.100
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 74.125.205.100
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 74.125.205.100
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
[ERROR] google.com IP mismatch: 74.125.205.100 New IP: 74.125.205.101 

yaml-file: 
drive.google.com: 173.194.222.194
google.com: 74.125.205.101
mail.google.com: 173.194.222.18

json-file: 
{"drive.google.com": "173.194.222.194", "mail.google.com": "173.194.222.18", "google.com": "74.125.205.101"}
--------------
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 74.125.205.101
drive.google.com - 173.194.222.194
mail.google.com - 173.194.222.18
google.com - 74.125.205.101
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
dns_ip.json
{"drive.google.com": "173.194.222.194", "mail.google.com": "173.194.222.18", "google.com": "74.125.205.101"}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
dns_yaml.yaml
drive.google.com: 173.194.222.194
google.com: 74.125.205.101
mail.google.com: 173.194.222.18
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys
import json
from builtins import input
from logging import fatal

import yaml

file = sys.argv[1]
is_file = os.path.isfile(file)
if is_file != True:
    print('Указанного файла не существует - проверьте путь')
    exit()

file_name, file_extension = os.path.splitext(file)
#print(file_extension)
if file_extension not in ('.yaml', '.json', '.yml'):
    print('Проверьте расширение файлов! Допустимы только \'.yaml\', \'.yml\', \'.json\'!')
    exit()

with open(file) as f1:
    is_json = f1.read()

is_json = is_json.strip()
#print(is_json)
is_json = is_json[0]+is_json[-1]
#print(is_json)
if is_json == '{}':
    print("Обнаружен синтаксис JSON! Преобразуем JSON->YAML")
    with open(file, 'r') as js1:
        try:
            buffer = json.load(js1)
            with open(file_name+'.yaml', 'w') as ym1:
                ym1.write(yaml.dump(buffer, explicit_start=True, explicit_end=True))
        except Exception as e:
            print(e)
else:
    print("Не обнаружен синтаксис JSON! Преобразуем YAML->JSON")
    with open(file, 'r') as ym1:
        try:
            buffer = yaml.safe_load(ym1)
            with open(file_name+'.json', 'w') as js1:
                js1.write(json.dumps(buffer, indent=2))
        except Exception as e:
            print(e)
#input('Press ENTER to exit')
```

---

### Пример работы скрипта №1:
```
PS C:\Users\Денис\PycharmProjects\dev-netology\04-script-03-yaml> python .\converter_json_yaml_json.py dns_ip_fake.json
Не обнаружен синтаксис JSON! Преобразуем YAML->JSON
```

#### Исходный файл: dns_ip_fake.json
```yaml
---
drive.google.com: 173.194.222.194
google.com: 74.125.205.101
mail.google.com: 173.194.222.18
...
```
#### Фвйл на выходе: dns_ip_fake.json
```json
{
  "drive.google.com": "173.194.222.194",
  "google.com": "74.125.205.101",
  "mail.google.com": "173.194.222.18"
}
```

---

### Пример работы скрипта №2:
```
PS C:\Users\Денис\PycharmProjects\dev-netology\04-script-03-yaml> python .\converter_json_yaml_json.py dns_ip_fake.yaml
Обнаружен синтаксис JSON! Преобразуем JSON->YAML
```
#### Исходный файл: dns_ip_fake.yaml
```json

{"drive.google.com": "173.194.222.194", "mail.google.com": "173.194.222.18", "google.com": "74.125.205.101"}

```
#### Фвйл на выходе: dns_ip_fake.yaml
```yaml
{
  "drive.google.com": "173.194.222.194",
  "google.com": "74.125.205.101",
  "mail.google.com": "173.194.222.18"
}
```

---

### Пример работы скрипта №3 (отработка ошибок):

#### Исходный файл: dns_ip_fake.json
```yaml
---
drive.google.com: 173.194.222.194
google.com: 74.125.205.101
mail.google.com: 173.194.222.18  трап
п
вм
цм
ва



...

```

#### Вывод консоли:
```
PS C:\Users\Денис\PycharmProjects\dev-netology\04-script-03-yaml> python .\converter_json_yaml_json.py dns_ip_fake.json
Не обнаружен синтаксис JSON! Преобразуем YAML->JSON
while scanning a simple key
  in "dns_ip_fake.json", line 5, column 1
could not find expected ':'
  in "dns_ip_fake.json", line 6, column 1

```

### Пример работы скрипта №3 (отработка ошибок):

#### Исходный файл: dns_ip_fake.json
```yaml
---
{
"drive.google.com: 173.194.222.194
"google.com": 74.125.205.101
"mail.google.com": 173.194.222.18
}
```

#### Вывод консоли:
```
PS C:\Users\Денис\PycharmProjects\dev-netology\04-script-03-yaml> python .\converter_json_yaml_json.py dns_ip.json
Обнаружен синтаксис JSON! Преобразуем JSON->YAML
Invalid control character at: line 2 column 35 (char 36)
```

