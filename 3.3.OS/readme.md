# Домашнее задание к занятию "3.3. Операционные системы, лекция 1""
 
1. Какой системный вызов делает команда cd? 
```bash 
vagrant@vagrant:~$ strace /bin/bash 'cd /tmp' 2>&1| grep cd
execve("/bin/bash", ["/bin/bash", "cd /tmp"], 0x7ffc754b1648 /* 24 vars */) = 0
ioctl(2, TIOCGPGRP, 0x7fff1899ecd4)     = -1 ENOTTY (Inappropriate ioctl for device)
openat(AT_FDCWD, "cd /tmp", O_RDONLY)   = -1 ENOENT (No such file or directory)
write(2, "/bin/bash: cd /tmp: No such file"..., 46/bin/bash: cd /tmp: No such file or directory
```
Ответ: openat

2. file ищет в : `/usr/share/misc/magic.mgc`
```bash 
strace file readme.md 2>&1 | grep openat
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libmagic.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/liblzma.so.5", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libbz2.so.1.0", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libz.so.1", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libpthread.so.0", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
openat(AT_FDCWD, "readme.md", O_RDONLY|O_NONBLOCK) = 3
```

3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

В любом случае при удалении (открытого) файла удаляется только ссылка на него, а сам файл остается с пометкой 'deleted'.

*Чтобы усечь его(существующий) перенаправлением:
`: > /path/to/the/file.log`

Если он уже был удален(наш вариант), то перенаправлением исправим:
`: > "/proc/$pid/fd/$fd"`

найти PID И удаленные файлы
```bash 
lsof -nP | grep ('deleted')
```

4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

Ответ: НЕТ, но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом. 

5. В iovisor BCC есть утилита opensnoop:
root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
/usr/sbin/opensnoop-bpfcc
На какие файлы вы увидели вызовы группы open за первую секунду работы утилиты? Воспользуйтесь пакетом bpfcc-tools для Ubuntu 20.04. Дополнительные сведения по установке.

Ответ:
```bash
vagrant@vagrant:~$ sudo /usr/sbin/opensnoop-bpfcc -d 1
PID    COMM               FD ERR PATH
858    vminfo              5   0 /var/run/utmp
585    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
585    dbus-daemon        18   0 /usr/share/dbus-1/system-services
585    dbus-daemon        -1   2 /lib/dbus-1/system-services
585    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/
```

6. Какой системный вызов использует uname -a? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в /proc, где можно узнать версию ядра и релиз ОС.

Ответ: `utsname`

`Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease,  version, domainname}. 

7. Чем отличается последовательность команд через ; и через && в bash? Например:
root@netology1:~# test -d /tmp/some_dir; echo Hi
Hi
root@netology1:~# test -d /tmp/some_dir && echo Hi
root@netology1:~#

Ответ: через ; выполняются обе команды последовательно, статус выхода - от последней команды. Через && - команда после && выполнится только если команда до && выполнится с статусом завершения 0(успех). Общий статус выхода - результат отработки всей конструкции.
```bash
vagrant@vagrant:~$ test -d /tmp/some_dir&& echo Hi
vagrant@vagrant:~$ echo $?
1
vagrant@vagrant:~$ test -d /tmp/some_dir; echo Hi
Hi
vagrant@vagrant:~$ echo $?
0
```
Есть ли смысл использовать в bash &&, если применить set -e? 

Ответ: ДА. Так как можно игнорировать ошибки в конвеере выполнения команд. В случае с && - команда справа от && СМОЖЕТ быть выполнена при даже при ошибке слева от &&. 

8. Из каких опций состоит режим bash set -euxo pipefail и почему его хорошо было бы использовать в сценариях?

ОТвет: Потому что В таком виде вывод это чистый дебаггер сценария, так как соответственно из опций: 
- e - немедленный выход, если команда завершается с ненулевым статусом конвеера
- u - при подстановке обрабатывать неустановленные переменные как ошибку -не выполнять конвеер
- x - печатает команды и их аргументы по мере их выполнения.
- o pipefail - возвращаемое значение конвейера - это статус последняя команда для выхода с ненулевым статусом, или ноль, если ни одна команда не завершилась с ненулевым статусом.

9. Используя -o stat для ps, определите, какой наиболее часто встречающийся статус у процессов в системе. В man ps ознакомьтесь (/PROCESS STATE CODES) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).
Ответ:   S - прерывистый сон (ожидает события для завершения)
```bash 
vagrant@vagrant:~$ ps -axo stat --no-header| sort | uniq -c -w 1 | sort -r
     45 S
     43 I
      1 R+
```

Для себя :
```bash
               D   -  uninterruptible sleep (usually IO)

               I    - Idle kernel thread
               R  -  running or runnable (on run queue)
               S  -  interruptible sleep (waiting for an event to complete)
               T   - stopped by job control signal
               t  -  stopped by debugger during the tracing
               W  -  paging (not valid since the 2.6.xx kernel)
               X  -  dead (should never be seen)
               Z  -  defunct ("zombie") process, terminated but not reaped by its parent

   For BSD formats and when the stat keyword is used, additional characters may be displayed:

               <    high-priority (not nice to other users)
               N    low-priority (nice to other users)
               L    has pages locked into memory (for real-time and custom IO)
               s    is a session leader
               l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
               +    is in the foreground process group
```
