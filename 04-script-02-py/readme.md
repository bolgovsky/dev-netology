### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-02-py/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | ошибка несоответствия типов в операции сложения (int и str)  |
| Как получить для переменной `c` значение 12?  |  c=str(a)+b , можно еще а='1', но по условию лектора "значения менять нельзя, тип- можно"  |
| Как получить для переменной `c` значение 3?  |   c=a+int(b) , можно еще b=2, но по условию лектора "значения менять нельзя, тип- можно" |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

Ответ: да, после первого нахождения 'modified' будет выполнен выход из сценария ( надо убрать 'break') и да, нет полного пути до измененных файлов (нужно добавлять префикс пути, в котором мы ищем изменения)

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
path='C:/Users/Денис/PycharmProjects/dev-netology/'
bash_command = ["cd "+path, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
#print('result_os = '+result_os)
is_change = False
for result in result_os.split('\n'):
    #print('result = '+result)
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(path+prepare_result)
        #break
input('Press ENTER to exit')
```

### Вывод скрипта при запуске при тестировании:
```
C:/Users/Денис/PycharmProjects/dev-netology/04-script-02-py/2.py
C:/Users/Денис/PycharmProjects/dev-netology/04-script-02-py/readme.md
Press ENTER to exit
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os
import sys

# path="C:/Users/Денис/PycharmProjects/dev-netology/"
path = sys.argv[1]
is_path = os.path.exists(path)
if is_path != True:
    print('Указанной папки не существует - проверьте путь')
    exit()

bash_command = ["cd " + path, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
#print('result_os = '+result_os)
is_change = False
for result in result_os.split('\n'):
    # print('result = '+result)
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(path + prepare_result)
        # break
input('Press ENTER to exit')
```

### Вывод скрипта при запуске при тестировании:
```
C:\Users\Денис\PycharmProjects\dev-netology\04-script-02-py>python 2.py C:\Users\Денис\PycharmProjects\dev-netology\04-script-02-py\
C:\Users\Денис\PycharmProjects\dev-netology\04-script-02-py\2.py
C:\Users\Денис\PycharmProjects\dev-netology\04-script-02-py\readme.md
Press ENTER to exit
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
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
```

### Вывод скрипта при запуске при тестировании:

Примечание: в определенный момент я просто очищал кэш DNS - 'ipconfig /flushdns'

```
C:\Users\Денис\PycharmProjects\dev-netology\04-script-02-py>python 4-socket.py
First resolving DNS-IP to set default values:
drive.google.com - 173.194.222.194
mail.google.com - 173.194.73.83
google.com - 74.125.205.102


drive.google.com - 173.194.222.194
mail.google.com - 173.194.73.83
google.com - 74.125.205.102
drive.google.com - 173.194.222.194
mail.google.com - 173.194.73.83
google.com - 74.125.205.102
drive.google.com - 173.194.222.194
mail.google.com - 173.194.73.83
[ERROR] google.com IP mismatch: 74.125.205.102 New IP: 74.125.205.113
drive.google.com - 173.194.222.194
[ERROR] mail.google.com IP mismatch: 173.194.73.83 New IP: 173.194.73.18
google.com - 74.125.205.113
drive.google.com - 173.194.222.194
mail.google.com - 173.194.73.18
```
