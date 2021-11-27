# Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"
 
1. cd - встроенная команда оболочки bash. То есть она описана внутри bash и не существует в файловой системе. 
```bash 
vagrant@vagrant:~$ type -t cd
builtin
```
2. Альтернатива `grep <some_string> <some_file> | wc -l`
```bash 
grep <some_string> <some_file> -с
```

3. Какой процесс с PID 1 является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?
```bash 
pstree -p
systemd(1)─┬─VBoxService(850)─┬─{VBoxService}(852)
           │                  ├─{VBoxService}(853)
           │                  ├─{VBoxService}(854)
           │                  ├─{VBoxService}(855)
           │                  ├─{VBoxService}(856)
           │                  ├─{VBoxService}(857)
           │                  ├─{VBoxService}(858)
           │                  └─{VBoxService}(859)
           ├─accounts-daemon(561)─┬─{accounts-daemon}(608)
           │                      └─{accounts-daemon}(612)
           ├─agetty(686)
           ├─atd(657)
           ├─cron(655)
           ├─dbus-daemon(563)
           ├─multipathd(511)─┬─{multipathd}(512)
           │                 ├─{multipathd}(513)
           │                 ├─{multipathd}(514)
           │                 ├─{multipathd}(515)
           │                 ├─{multipathd}(516)
           │                 └─{multipathd}(517)
           ├─networkd-dispat(571)
           ├─polkitd(630)─┬─{polkitd}(631)
           │              └─{polkitd}(633)
           ├─rpcbind(538)
           ├─rsyslogd(572)─┬─{rsyslogd}(584)
           │               ├─{rsyslogd}(585)
           │               └─{rsyslogd}(586)
           ├─sshd(688)───sshd(1066)───sshd(1113)───bash(1114)───pstree(1330)
           ├─systemd(1079)───(sd-pam)(1080)
           ├─systemd-journal(352)
           ├─systemd-logind(575)
           ├─systemd-network(383)
           ├─systemd-resolve(539)
           └─systemd-udevd(378)
```
Это процесс `systemd` - менеджер системы и служб для Linux, совместимый со скриптами инициализации SysV и LSB

4. Как будет выглядеть команда, которая перенаправит вывод stderr ls на другую сессию терминала?
Требуется еще одна сессия терминала и повышение полномочий(sudo su)
```bash
ls 2>/dev/pts1
```
5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.
Ответ: ДА. Пример:
```bash
grep b 0<readme.md 1>readme.txt
```

6. Получится ли находясь в графическом режиме, вывести данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?

Ответ: ДА и ДА(в теминале tty).Необходимо для начала создать tty(открыть сессию терминала VirtualBox) и pty(ssh).
Соответственно из pty выполняем:
```bash
vagrant@vagrant:~$ tty
/dev/pts/0
vagrant@vagrant:~$ echo hi >/dev/tty1
```
и в tty наблюдаем вывод:
```bash
vagrant@vagrant:~$ tty
/dev/tty1
vagrant@vagrant:`$ hi

```

7. Выполните команду bash 5>&1. К чему она приведет? 
```bash
vagrant@vagrant:~$ lsof -p $$ | grep /dev/pts/0
bash    1664 vagrant    0u   CHR  136,0      0t0      3 /dev/pts/0
bash    1664 vagrant    1u   CHR  136,0      0t0      3 /dev/pts/0
bash    1664 vagrant    2u   CHR  136,0      0t0      3 /dev/pts/0
bash    1664 vagrant  255u   CHR  136,0      0t0      3 /dev/pts/0
vagrant@vagrant:~$ bash 5>&1
vagrant@vagrant:~$ lsof -p $$ | grep /dev/pts/0
bash    1729 vagrant    0u   CHR  136,0      0t0      3 /dev/pts/0
bash    1729 vagrant    1u   CHR  136,0      0t0      3 /dev/pts/0
bash    1729 vagrant    2u   CHR  136,0      0t0      3 /dev/pts/0
bash    1729 vagrant    5u   CHR  136,0      0t0      3 /dev/pts/0
bash    1729 vagrant  255u   CHR  136,0      0t0      3 /dev/pts/0
```
Ответ: создание и перенаправление пользовательского  фалового дескриптора (5) в стандартный поток вывода(1).

Что будет, если вы выполните echo netology > /proc/$$/fd/5? Почему так происходит? 
Ответ: произойдет перенаправление потока вывода echo в только что созданный файловый дескриптор(5). /proc/$$/fd/5 -  представление созданного файлового дескриптора, хранящееся в псевдофайловой системе /proc.

8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от | на stdin команды справа. Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.

ОТвет: ДА.
```bash
vagrant@vagrant:~$ bash 5>&2 2>&1 1>&5
```

9. Что выведет команда `cat /proc/$$/environ`? Как еще можно получить аналогичный по содержанию вывод?

Ответ: выводит переменные окружения(параметры) текущей сессии терминала. Аналог - команда `env -0`, хотя нагляднее использовать  `xargs -0 -L1 -a /proc/$$/environ` и `env` соответственно.

11. Используя man, опишите что доступно по адресам:

/proc/<PID>/cmdline - команда, которой был запущен процесс с идентификатором <PID>, если только процесс не является зомби (тогда вернет 0 символов).

/proc/<PID>/exe - символическая ссылка на исполняемый файл программы.

13. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью /proc/cpuinfo.

Ответ: 4.2
```baSH
vagrant@vagrant:~$ cat /proc/cpuinfo | grep sse
flags   : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr ss
 sse2 ht syscall nx rdtscp lm constant_tsc rep_good nopl xtopology nonstop_tsc cpuid tsc_known_freq pni pclmulqdq monitor ssse3 cx16 pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx rdrand hypervisor lahf_lm abm 3dnowprefetch invpcid_single fsgsbase avx2 invpcid rdseed clflushopt md_clear flush_l1d arch_capabilities
```

12. При открытии нового окна терминала и vagrant ssh создается новая сессия и выделяется pty. Это можно подтвердить командой tty, которая упоминалась в лекции 3.2. Однако:
```baSH
vagrant@netology1:~$ ssh localhost 'tty'
not a tty
```
Почитайте, почему так происходит, и как изменить поведение.

Ответ: `man ssh`, `https://unix.stackexchange.com/questions/48527/ssh-inside-ssh-fails-with-stdin-is-not-a-tty` 
- по умолчанию tty не создается для запуска команды с помощью ssh.Это позволяет передавать двоичные данные и т. Д., Не сталкиваясь с причудами TTY. Однако, когда вы запускаете ssh без удаленной команды, он ДЕЙСТВИТЕЛЬНО выделяет TTY, потому что вы, вероятно, будете запускать сеанс оболочки. 

- Для принудительного запуска tty нужно использовать `ssh -t localhost 'tty'`.

13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись reptyr. Например, так можно перенести в screen процесс, который вы запустили по ошибке в обычной SSH-сессии.

Ответ: 
```bash
apt-get install reptyr
sudo sysctl -w kernel.yama.ptrace_scope=0 # тобы не перезагружаться
yes wake up neo
Ctrl+Z # Приостановить  процесс 
top -d 999 
L yes  # находим PID 
Ctrl+С
screen -S test_reptyr # создаем именованный виртуальный терминал куда будем переносить
reptyr PID # восстанавливаем процесс здесь (test_reptyr)  
```

14. sudo echo string > /root/new_file не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без sudo под вашим пользователем. Для решения данной проблемы можно использовать конструкцию echo string | sudo tee /root/new_file. Узнайте что делает команда tee и почему в отличие от sudo echo команда с sudo tee будет работать.

Ответ: tee -  выводит на экран или же перенаправляет выходной материал команды и копирует его в файл или в переменную. Если echo - встроенная команда в оболочку bash(то есть sudo не сработает- надо запускать сам bash под sudo), то является внешней командой и для нее выполнение повышеия привилегий допустимо.  