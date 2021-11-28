# Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"

5. Какие ресурсы выделены по-умолчанию? cpu = 2 , memory = 1024 
6. Как добавить оперативной памяти или ресурсов процессора виртуальной машине? -> дописать в конф. файл vagrntfile строки с настройками :
```bash 
  config.vm.provider "virtualbox" do |vb|
	  #   # Display the VirtualBox GUI when booting the machine
	  vb.name = "ubuntu20.04"
	  #vb.gui = true
	  #
	  #   # Customize the amount of memory on the VM:
	  vb.customize ["modifyvm", :id, "--cpuexecutioncap", "20"]
	  vb.memory = 512
	  vb.cpus = 1 
  end 
```
8. какой переменной можно задать длину журнала history, и на какой строчке manual это описывается? ->
 HISTSIZE , по-умолчанию 500 , найдено в строке 621

что делает директива ignoreboth в bash? -> если задать параметру HISTCONTROL значение ignoreboth, то в историю команд не будут писаться команды , которые начинаются с пробела и повторяющиеся

9. В каких сценариях использования применимы скобки {} и на какой строчке man bash это описано? -> в сценариях группировки комманд для запуска в текущем окружении оболочки, на строчке 165.
10. как создать однократным вызовом touch 100000 файлов? -> 
```bash
touch {1..100000}
```
Получится ли аналогичным образом создать 300000? Если нет, то почему?-> Аналогичным способом не получится, потому что есть ограничение на длину передаваемых аргументов в функцию, установленное по умолчанию.

11. В man bash поищите по /\[\[. Что делает конструкция [[ -d /tmp ]] ->  проверка условного выражения , что /tmp существует и является директорией.

12. Ответ:
```bash
mkdir /tmp/new_path_directory
cp /usr/bin/bash /tmp/new_path_directory
PATH=/tmp/new_path_directory:$PATH
```

13. at - одноразовый запуск задачи по расписанию(по времени)
batch - тоже самое , но по допустимому уровню загрузки системы