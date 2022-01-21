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
try:
    result_os = os.popen(' && '.join(bash_command)).read()
except :
    result_os = ''
print("Что-то пошло не так - скорее всего папка не является git-репозиторием!")
#print('result_os = '+result_os)
is_change = False
for result in result_os.split('\n'):
    # print('result = '+result)
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(path + prepare_result)
        # break
input('Press ENTER to exit')