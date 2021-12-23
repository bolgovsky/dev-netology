# Домашнее задание к занятию "3.5. Файловые системы"
 
1. Разрежённый файл (англ. sparse file) — файл, в котором последовательности нулевых байтов[1] заменены на информацию об этих последовательностях (список дыр).

2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?
 
Ответ: нет, так как жёсткие ссылки не являются самостоятельными файлами и имеют те же права доступа и владельца, что и файл.

3. Используя fdisk, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
```bash 
vagrant@vagrant:~$ sudo fdisk  /dev/sdb
Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 1
First sector (2048-5242879, default 2048):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2048M

Created a new partition 1 of type 'Linux' and of size 2 GiB.
Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (2-4, default 2):
First sector (4196352-5242879, default 4196352):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):

Created a new partition 2 of type 'Linux' and of size 511 MiB.
...
Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 4196351 4194304    2G 83 Linux
/dev/sdb2       4196352 5242879 1046528  511M 83 Linux
```

5. Используя sfdisk, перенесите данную таблицу разделов на второй диск.
```bash 
vagrant@vagrant:~$ sudo sfdisk --dump /dev/sdb > sda.dump
vagrant@vagrant:~$ sudo sfdisk /dev/sdc < sda.dump
Checking that no-one is using this disk right now ... OK
```

6. Соберите mdadm RAID1 на паре разделов 2 Гб.
```bash 
mdadm --create --verbose /dev/md127 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

```

7. Соберите mdadm RAID0 на второй паре маленьких разделов.
```bash 
mdadm --create --verbose /dev/md126 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2
```

8. Создайте 2 независимых PV на получившихся md-устройствах.
```bash 
sudo pvcreate /dev/md127 /dev/md126

sudo pvs
  PV         VG        Fmt  Attr PSize    PFree
  /dev/md126           lvm2 ---  1018.00m 1018.00m
  /dev/md127           lvm2 ---    <2.00g   <2.00g
  /dev/sda5  vgvagrant lvm2 a--   <63.50g       0
```

9. Создайте общую volume-group на этих двух PV.
```bash 
vagrant@vagrant:~$ sudo vgcreate volume-group /dev/md126 /dev/md127
  Volume group "volume-group" successfully created
vagrant@vagrant:~$ sudo vgs
  VG           #PV #LV #SN Attr   VSize   VFree
  vgvagrant      1   2   0 wz--n- <63.50g     0
  volume-group   2   0   0 wz--n-  <2.99g <2.99g
```

10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.
 ```bash 
sudo lvcreate -L 100M -n LV volume-group /dev/md126

sudo lvs
  LV     VG           Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  root   vgvagrant    -wi-ao---- <62.54g                               
  swap_1 vgvagrant    -wi-ao---- 980.00m                               
  LV     volume-group -wi-a----- 100.00m
```

11. Создайте mkfs.ext4 ФС на получившемся LV.
```bash 
sudo mkfs.ext4 /dev/volume-group/LV
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done
Writing inode tables: done
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done
```

13. Смонтируйте этот раздел в любую директорию, например, /tmp/new.
```bash 
vagrant@vagrant:/tmp$ sudo mount /dev/volume-group/LV /tmp/new
```

15. Поместите туда тестовый файл, например wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz.
```bash 
vagrant@vagrant:/tmp$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2021-12-23 18:38:52--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 21546631 (21M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz             100%[==============================================>]  20.55M  3.19MB/s    in 6.0s

2021-12-23 18:38:58 (3.44 MB/s) - ‘/tmp/new/test.gz’ saved [21546631/21546631]
```

14 .Прикрепите вывод lsblk.
```bash 
vagrant@vagrant:/tmp/new$ lsblk
NAME                   MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                      8:0    0   64G  0 disk
├─sda1                   8:1    0  512M  0 part  /boot/efi
├─sda2                   8:2    0    1K  0 part
└─sda5                   8:5    0 63.5G  0 part
  ├─vgvagrant-root     253:0    0 62.6G  0 lvm   /
  └─vgvagrant-swap_1   253:1    0  980M  0 lvm   [SWAP]
sdb                      8:16   0  2.5G  0 disk
├─sdb1                   8:17   0    2G  0 part
│ └─md127                9:127  0    2G  0 raid1
└─sdb2                   8:18   0  511M  0 part
  └─md126                9:126  0 1018M  0 raid0
    └─volume--group-LV 253:2    0  100M  0 lvm   /tmp/new
sdc                      8:32   0  2.5G  0 disk
├─sdc1                   8:33   0    2G  0 part
│ └─md127                9:127  0    2G  0 raid1
└─sdc2                   8:34   0  511M  0 part
  └─md126                9:126  0 1018M  0 raid0
    └─volume--group-LV 253:2    0  100M  0 lvm   /tmp/new
```

15. Протестируйте целостность файла:
```bash
vagrant@vagrant:/tmp/new$ gzip -t /tmp/new/test.gz
vagrant@vagrant:/tmp/new$ echo $?
0
```

16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.
```bash
vagrant@vagrant:/tmp/new$ sudo pvmove /dev/md126 /dev/md127
  /dev/md126: Moved: 20.00%

  /dev/md126: Moved: 100.00%
```

17. Сделайте --fail на устройство в вашем RAID1 md.
```bash
sudo mdadm --manage /dev/md127 --fail /dev/sdb1


18. Подтвердите выводом dmesg, что RAID1 работает в деградированном состоянии.
```bash
dmesg
[ 5823.832867] md/raid1:md127: Disk failure on sdb1, disabling device.
               md/raid1:md127: Operation continuing on 1 devices.
```

19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:
```bash
vagrant@vagrant:/tmp/new$ gzip -t /tmp/new/test.gz;echo $?
0
```
20. Погасите тестовый хост, vagrant destroy.