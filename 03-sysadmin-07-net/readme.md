# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

---

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

Linux
```bash
ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:73:60:cf brd ff:ff:ff:ff:ff:ff
```
Windows
```bash
ipconfig

Настройка протокола IP для Windows


Адаптер Ethernet Ethernet:

   Состояние среды. . . . . . . . : Среда передачи недоступна.
   DNS-суффикс подключения . . . . . :

Адаптер Ethernet vEthernet (WSL):

   DNS-суффикс подключения . . . . . :
   Локальный IPv6-адрес канала . . . : fe80::3457:d6f9:3401:f8ae%21
   IPv4-адрес. . . . . . . . . . . . : 172.29.176.1
   Маска подсети . . . . . . . . . . : 255.255.240.0
   Основной шлюз. . . . . . . . . :

Адаптер Ethernet Ethernet 2:

   DNS-суффикс подключения . . . . . :
   Локальный IPv6-адрес канала . . . : fe80::71c3:2295:61b1:fe23%23
   IPv4-адрес. . . . . . . . . . . . : 192.168.56.1
   Маска подсети . . . . . . . . . . : 255.255.255.0
   Основной шлюз. . . . . . . . . :```
```

---

2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

**CDP (англ. Cisco Discovery Protocol)** — проприетарный протокол второго уровня, разработанный компанией Cisco Systems, позволяющий обнаруживать подключённое (напрямую или через устройства первого уровня) сетевое оборудование Cisco, его название, версию IOS и IP-адреса.

**Link Layer Discovery Protocol (LLDP)** — протокол канального уровня, позволяющий сетевому оборудованию оповещать оборудование, работающее в локальной сети, о своём существовании и передавать ему свои характеристики, а также получать от него аналогичные сведения. 
```bash
lldpctl
-------------------------------------------------------------------------------
LLDP neighbors:
-------------------------------------------------------------------------------
```

---

3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей?  

**VLAN (аббр. от англ. Virtual Local Area Network)** — виртуальная локальная компьютерная сеть.

Какой пакет и команды есть в Linux для этого?
Пакет -  ``vlan`` , описание: [http://xgu.ru/wiki/VLAN_%D0%B2_Ubuntu](http://xgu.ru/wiki/VLAN_%D0%B2_Ubuntu)
Утилиты: `vconfig` `ip link`

Приведите пример конфига.
```bash
vi /etc/network/interfaces

auto vlan1400
iface vlan1400 inet static
        address 192.168.1.1
        netmask 255.255.255.0
        vlan_raw_device eth0
```

---


4. Какие типы агрегации интерфейсов есть в Linux? 
* Статическое агрегирование:

Преимущества:
Не вносит дополнительную задержку при поднятии агрегированного канала или изменении его настроек
Вариант, который рекомендует использовать Cisco

Недостатки:
Нет согласования настроек с удаленной стороной. Ошибки в настройке могут привести к образованию петель

* (Динамическое)Агрегирование с помощью LACP:

Преимущества:
Согласование настроек с удаленной стороной позволяет избежать ошибок и петель в сети.
Поддержка standby-интерфейсов позволяет агрегировать до 16ти портов, 8 из которых будут активными, а остальные в режиме standby

Недостатки:
Вносит дополнительную задержку при поднятии агрегированного канала или изменении его настроек


Какие опции есть для балансировки нагрузки?
* **Mode-0(balance-rr)** – Данный режим используется по умолчанию. Balance-rr обеспечивается балансировку нагрузки и отказоустойчивость. В данном режиме сетевые пакеты отправляются “по кругу”, от первого интерфейса к последнему. Если выходят из строя интерфейсы, пакеты отправляются на остальные оставшиеся. Дополнительной настройки коммутатора не требуется при нахождении портов в одном коммутаторе. При разностных коммутаторах требуется дополнительная настройка.

* **Mode-1(active-backup)** – Один из интерфейсов работает в активном режиме, остальные в ожидающем. При обнаружении проблемы на активном интерфейсе производится переключение на ожидающий интерфейс. Не требуется поддержки от коммутатора.

* **Mode-2(balance-xor)** – Передача пакетов распределяется по типу входящего и исходящего трафика по формуле ((MAC src) XOR (MAC dest)) % число интерфейсов. Режим дает балансировку нагрузки и отказоустойчивость. Не требуется дополнительной настройки коммутатора/коммутаторов.

* **Mode-3(broadcast)** – Происходит передача во все объединенные интерфейсы, тем самым обеспечивая отказоустойчивость. Рекомендуется только для использования MULTICAST трафика.

* **Mode-4(802.3ad)** – динамическое объединение одинаковых портов. В данном режиме можно значительно увеличить пропускную способность входящего так и исходящего трафика. Для данного режима необходима поддержка и настройка коммутатора/коммутаторов.

* **Mode-5(balance-tlb)** – Адаптивная балансировки нагрузки трафика. Входящий трафик получается только активным интерфейсом, исходящий распределяется в зависимости от текущей загрузки канала каждого интерфейса. Не требуется специальной поддержки и настройки коммутатора/коммутаторов.

* **Mode-6(balance-alb)** – Адаптивная балансировка нагрузки. Отличается более совершенным алгоритмом балансировки нагрузки чем Mode-5). Обеспечивается балансировку нагрузки как исходящего так и входящего трафика. Не требуется специальной поддержки и настройки коммутатора/коммутаторов.

Приведите пример конфига.
```bash 
vi  /etc/network/interfaces

auto enp2s0
iface enp2s0 inet manual

auto enp2s1
iface enp2s1 inet manual

auto bond0
iface bond0 inet static
address 10.10.10.1/24
gateway 10.10.10.254
dns-nameservers 10.10.10.10 10.10.10.11
slaves enp2s0 enp2s1
bond-mode 802.3ad
bond-lacp-rate slow
```

---


5.Сколько IP адресов в сети с маской /29 ? 

Ответ: шесть + один широковещательный(.7) + один сети (.0)
```bash 
ipcalc 192.168.1.1/29
Address:   192.168.1.1          11000000.10101000.00000001.00000 001
Netmask:   255.255.255.248 = 29 11111111.11111111.11111111.11111 000
Wildcard:  0.0.0.7              00000000.00000000.00000000.00000 111
=>
Network:   192.168.1.0/29       11000000.10101000.00000001.00000 000
HostMin:   192.168.1.1          11000000.10101000.00000001.00000 001
HostMax:   192.168.1.6          11000000.10101000.00000001.00000 110
Broadcast: 192.168.1.7          11000000.10101000.00000001.00000 111
Hosts/Net: 6
```
Сколько /29 подсетей можно получить из сети с маской /24. 

Ответ: 32
```bash 
ipcalc -b 10.10.10.0/24 /29
...
Subnets:   32
```

Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
```bash
 31.
Network:   10.10.10.240/29
HostMin:   10.10.10.241
HostMax:   10.10.10.246
Broadcast: 10.10.10.247
Hosts/Net: 6                     Class A, Private Internet

 32.
Network:   10.10.10.248/29
HostMin:   10.10.10.249
HostMax:   10.10.10.254
Broadcast: 10.10.10.255
Hosts/Net: 6
```

---


6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? 

Ответ: из частной подсети 100.64.0.0 — 100.127.255.255 (маска подсети: 255.192.0.0 или /10) Carrier-Grade NAT

Маску выберите из расчета максимум 40-50 хостов внутри подсети.

Ответ: маска /26 - в данном случае емкость хостов 64 
```bash 
ipcalc -s 40 100.64.0.0/10
Address:   100.64.0.0           01100100.01 000000.00000000.00000000
Netmask:   255.192.0.0 = 10     11111111.11 000000.00000000.00000000
Wildcard:  0.63.255.255         00000000.00 111111.11111111.11111111
=>
Network:   100.64.0.0/10        01100100.01 000000.00000000.00000000
HostMin:   100.64.0.1           01100100.01 000000.00000000.00000001
HostMax:   100.127.255.254      01100100.01 111111.11111111.11111110
Broadcast: 100.127.255.255      01100100.01 111111.11111111.11111111
Hosts/Net: 4194302               Class A

1. Requested size: 40 hosts
Netmask:   255.255.255.192 = 26 11111111.11111111.11111111.11 000000
Network:   100.64.0.0/26        01100100.01000000.00000000.00 000000
HostMin:   100.64.0.1           01100100.01000000.00000000.00 000001
HostMax:   100.64.0.62          01100100.01000000.00000000.00 111110
Broadcast: 100.64.0.63          01100100.01000000.00000000.00 111111
Hosts/Net: 62                    Class A

Needed size:  64 addresses.
Used network: 100.64.0.0/26

```

---

7. Как проверить ARP таблицу в Linux, Windows?  

Linux `ip neighbour`

Windows `arp -a`

Как очистить ARP кеш полностью?

Linux ` ip neigh flush all `

Windows `arp -d *`

Как из ARP таблицы удалить только один нужный IP?

Linux `ip neighbour delete IP`

Windows `arp -d IP`