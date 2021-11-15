###Домашнее задание к занятию «2.4. Инструменты Git»


Для выполнения заданий в этом разделе давайте склонируем репозиторий с исходным кодом терраформа https://github.com/hashicorp/terraform
    
    git clone https://github.com/hashicorp/terraform.git terraform

<br>
В виде результата напишите текстом ответы на вопросы и каким образом эти ответы были получены.

---

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea. 

Ответ:<b> `aefead2207ef7e2aa5dc81a34aedf0cad4c32545` </b>

```bash
git show aefea
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
```

---

2. Какому тегу соответствует коммит 85024d3?

Ответ:<b>`v0.12.23`</b>

```bash
git show 85024d3
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
```

---

3. Сколько родителей у коммита b8d720? Напишите их хеши.

Ответ:<b>`ДВА РОДИТЕЛЯ`: `56cd7859e05c36c06b56d013b55a252d0bb7e158`, `9ea88f22fc6269854151c571162c5bcf958bee2b`</b>

```bash
git show b8d720^@ --oneline
56cd7859e Merge pull request #23857 from hashicorp/cgriggs01-stable
9ea88f22f add/update community provider listings
```

Еще способ: перебрать ^,^2,^3, ... до ошибки, проверим:

```bash 
git show b8d720^2 --oneline
git show b8d720^3
fatal: ambiguous argument 'b8d720^3': unknown revision or path not in the working tree.
```

Еще способ: отобразить дерево коммитов по хэшу и просто посмотреть:

```bash
git log --oneline --graph b8d720
*   b8d720f83 Merge pull request #23916 from hashicorp/cgriggs01-stable
|\
| * 9ea88f22f add/update community provider listings
|/
*   56cd7859e Merge pull request #23857 from hashicorp/cgriggs01-stable
```

---

4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.<br>

Ответ:


<table align="left" style='font-family:"Courier New", Courier, monospace; font-size:80%'>
    <tr> 
        <td align="center"> <b>HASH </td><td align="center"> <b> COMMIT </td>
    </tr>
    <tr> 
        <td> b14b74c4939dcab573326f4e3ee2a62e23e12f89 </td><td>  [Website] vmc provider links </td>
    </tr>
    <tr>
        <td> 3f235065b9347a758efadc92295b540ee0a5e26e </td><td>  Update CHANGELOG.md </td>
    </tr>
    <tr>
        <td> 6ae64e247b332925b872447e9ce869657281c2bf </td><td>  registry: Fix panic when server is unreachable </td>
    </tr>
    <tr>
        <td> 5c619ca1baf2e21a155fcdb4c264cc9e24a2a353 </td><td>  website: Remove links to the getting started guide's old location </td>
    </tr>
    <tr>
        <td> 06275647e2b53d97d4f0a19a0fec11f6d69820b5 </td><td>  Update CHANGELOG.md </td>
    </tr>
    <tr> 
        <td> d5f9411f5108260320064349b757f55c09bc4b80 </td><td>  command: Fix bug when using terraform login on Windows </td>
    </tr>
    <tr>  
        <td> 4b6d06cc5dcb78af637bbb19c198faff37a066ed </td><td>  Update CHANGELOG.md </td>
    </tr>
    <tr> 
        <td> dd01a35078f040ca984cdd349f18d0b67e486c35 </td><td>  Update CHANGELOG.md </td>
    </tr>
    <tr> 
        <td> 225466bc3e5f35baa5d07197bbc079345b77525e </td><td>  Cleanup after v0.12.23 release </td>
    </tr>
</table>

<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

Здесь для вывода прямо по заданию надо использовать функцию форматирования вывода и убрать лишнюю строчку коммита крайнего тега:

```bash
    git log --pretty=format:'%H %s' v0.12.23..v0.12.24
```

---

5. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).<br>

Ответ: 

<b> `8c928e83589d90a031f811fae52a81be7153e82f` </b> <br><br>

Для начала найдём В КАКИХ ФАЙЛАХ вообще искать данную функцию: 

```bash
git grep 'func providerSource'
provider_source.go:func providerSource(configs []*cliconfig.ProviderInstallation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
provider_source.go:func providerSourceForCLIConfigLocation(loc cliconfig.ProviderInstallationLocation, services *disco.Disco) (getproviders.Source, tfdiags.Diagnostics) {
```

Видим: наш клиент- в первой строке! <br>

Значит ищем в файле `provider_source.go` первый коммит с упоминанием данной функции (без сокращений- будем листать и искать самую раннюю дату коммита- они в обратном порядке выводятся!):

```bash
git log -L :providerSource:provider_source.go
commit 5af1e6234ab6da412fb8637393c5a17a1b293663
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Tue Apr 21 16:28:59 2020 -0700

    main: Honor explicit provider_installation CLI config when present

...

commit 8c928e83589d90a031f811fae52a81be7153e82f
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Thu Apr 2 18:04:39 2020 -0700

    main: Consult local directories as potential mirrors of providers
...
+func providerSource(services *disco.Disco) getproviders.Source {
+       // We're not yet using the CLI config here because we've not implemented
+       // yet the new configuration constructs to customize provider search
+       // locations. That'll come later.
+       // For now, we have a fixed set of search directories:
(END)
```

---

6. Найдите все коммиты в которых была изменена функция globalPluginDirs.<br>

Ответ:

<table align="left" style='font-family:"Courier New", Courier, monospace; font-size:80%'>
    <tr> 
        <td align="center"> <b> COMMIT </td>
    </tr>
    <tr> 
        <td align="left"> Remove config.go and update things using its aliases</td>
    </tr>
    <tr> 
        <td align="left"> keep .terraform.d/plugins for discovery</td>
    </tr>
    <tr> 
        <td align="left"> Add missing OS_ARCH dir to global plugin paths </td>
    </tr>
    <tr> 
        <td align="left"> move some more plugin search path logic to command </td>
    </tr>
    <tr> 
        <td align="left"> Push plugin discovery down into command package </td>
    </tr>
</table>

<br><br><br><br><br><br><br><br><br><br><br><br><br>

Делаем все по аналогии с п.5, но удобнее вывод сокращенный:

```bash
git log  -L :globalPluginDirs:plugins.go --pretty=oneline
```

7. Кто автор функции synchronizedWriters?

Ответ: `Author: Martin Atkins <mart@degeneration.co.uk>`

Стандартным способом найти не удалось, ищем в истории:

```bash
git log -S"synchronizedWriters" --oneline
bdfea50cc remove unused
fd4f7eb0b remove prefixed io
5ac311e2a main: synchronize writes to VT100-faker on Windows
```

Помним про порядок вывода-смотрим первую запись и проверяем + и - в diff-ах: 

```bash
git show 5ac311e2a
+func synchronizedWriters(targets ...io.Writer) []io.Writer {
  ...
git show bdfea50cc
-func synchronizedWriters(targets ...io.Writer) []io.Writer {
}
```

Поэтому и не находилась grep-ом как я понял-была удалена.