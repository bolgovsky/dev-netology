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