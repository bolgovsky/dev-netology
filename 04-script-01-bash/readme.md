# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## Обязательная задача 1

Есть скрипт:
```bash
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))
```
Ответ:
```
vagrant@vagrant:~$ echo $c $d $e
a+b 1+2 3
```

Какие значения переменным c,d,e будут присвоены? Почему?

| Переменная  | Значение | Обоснование |
| ------------- | ------------- | ------------- |
| `c`  | a+b  | тип по умолчанию-стока+нет доступа к значению переменных  |
| `d`  | 1+2  | есть доступ к значению переменных, но не выражения- снова строка |
| `e`  | 3  | есть доступ к значениям переменных и выражения - тип целочисленный|


## Обязательная задача 2
На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным (после чего скрипт должен завершиться). В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:

Ответ: закрываем скобки в цикле while, добавляем `sleep 1` в тело цикла для проверки раз в секунду (либо заменить `>>` на `>`, чтобы перезаписывать лог и не расходовать место на жестком диске) и добавляем условие для выхода из скрипта при доступности сервиса:
```bash
while ((1==1))
do
	curl https://localhost:4757
	if (($? != 0))
	then
		date >> curl.log
	else exit
	fi
	sleep 1
done
```

Необходимо написать скрипт, который проверяет доступность трёх IP: `192.168.0.1`, `173.194.222.113`, `87.250.250.242` по `80` порту и записывает результат в файл `log`. Проверять доступность необходимо пять раз для каждого узла.

### Ваш скрипт:
```bash
vi script.sh

#!/usr/bin/env bash
array_ip=(192.168.0.1 173.194.222.113 87.250.250.242)
for ((i=0;i<5;i++))
 do
   for ip in ${array_ip[@]}
    do 
      (date; nc -zv -w1  $ip 80 2>&1) >>  $ip.log 
    done 
done

./script

ls *.log
173.194.222.113.log  192.168.0.1.log  87.250.250.242.log



vagrant@vagrant:~$ array_ip=(192.168.0.1 173.194.222.113 87.250.250.242)
vagrant@vagrant:~$    for ip in ${array_ip[@]}
>     do
>       echo
>       echo $ip
>       cat $ip.log
>     done

192.168.0.1
Thu 13 Jan 2022 09:12:43 PM UTC
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
Thu 13 Jan 2022 09:12:44 PM UTC
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
Thu 13 Jan 2022 09:12:45 PM UTC
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
Thu 13 Jan 2022 09:12:46 PM UTC
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
Thu 13 Jan 2022 09:12:47 PM UTC
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress

173.194.222.113
Thu 13 Jan 2022 09:12:44 PM UTC
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:45 PM UTC
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:46 PM UTC
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:47 PM UTC
Connection to 173.194.222.113 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:48 PM UTC
Connection to 173.194.222.113 80 port [tcp/http] succeeded!

87.250.250.242
Thu 13 Jan 2022 09:12:44 PM UTC
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:45 PM UTC
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:46 PM UTC
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:47 PM UTC
Connection to 87.250.250.242 80 port [tcp/http] succeeded!
Thu 13 Jan 2022 09:12:48 PM UTC
Connection to 87.250.250.242 80 port [tcp/http] succeeded!

```

## Обязательная задача 3
Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается.

### Ваш скрипт:
```bash
vi 2script.sh

#!/usr/bin/env bash
array_ip=(173.194.222.113 87.250.250.242 192.168.0.1)
while (( 1==1 ))
do
  for ip in ${array_ip[@]}
  do
        nc -zv -w1  $ip 80 2>&1
        if (($? != 0))
        then
                echo $ip>ip.log
                exit 0
        fi
  done
done

vagrant@vagrant:~$ ./2script.sh
nc: connect to 192.168.0.1 port 80 (tcp) timed out: Operation now in progress
vagrant@vagrant:~$ cat ip.log
192.168.0.1
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Мы хотим, чтобы у нас были красивые сообщения для коммитов в репозиторий. Для этого нужно написать локальный хук для git, который будет проверять, что сообщение в коммите содержит код текущего задания в квадратных скобках и количество символов в сообщении не превышает 30. Пример сообщения: \[04-script-01-bash\] сломал хук.

### Ваш скрипт:
```bash
 echo [04-script-01-bash] | awk '/(^\[[0-9][0-9]-([a-zA-Z0-9].*)\]-([a-zA-Z0-9].*)){0,30}$/'
 [04-script-01-bash] 
 
```

```
vi .git\hooks\commit-msg 

#!/bin/sh

TEXT=$(cat "$1" | awk '/(^\[[0-9][0-9]-([a-zA-Z0-9].*)\]-([a-zA-Z0-9].*)){0,30}$/')

if [ -n "$TEXT" ]
then
       echo "" >> "$1"
       echo $TEXT >> "$1"
else
    echo "[POLICY] Aborting commit due to empty commit message or content."
    exit 1
fi

adde

```