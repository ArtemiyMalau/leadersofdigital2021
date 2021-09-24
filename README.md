<p align="center">
<h4>Реализованная функциональность</h4>
<ul>
    <li>Защищенная Авторизация и Регистрация;</li>
    <li>Возможна регистрация как заказчика, так и изготовоителя;</li>
    <li>Поиск изготовоителей по ОКВЭД кодам;</li>
    <li>Поиск изготовоителей по городам России;</li>
    <li>Поиск изготовоителей по названию компании;</li>
    <li>Возможность отправки писма на почту определенному производителю с целью дальнейшего взаимодействия посредством общения в мессенджере нашего веб-приложения;</li>
    <li>Личный кабинет пользователя с информаицей о запросах отправленных производителям и закладками карточек изготовителей;</li>
    <li>Возможность смены всей информации о пользователе в личном кабинете;</li> 
</ul> 
<h4>Особенность проекта в следующем:</h4>
<ul>
<li>Уникальный алгоритм посчета рейтинга для производителся, основанный на финансовом состоянии компании;</li>
 <li>При поиске генерируется шорт лист "рекомендуемых поставщиков" основаный на рейтинге производителя и лонг лист со всеми доступными производителми;</li>
 </ul>
<h4>Основной стек технологий:</h4>
<ul>
  <li>LAMP</li>
	<li>HTML, CSS, JavaScript, WebSocket.</li>
	<li>PHP 7, MySQL, Python</li>
	<li>SQLAlchemy, Selenium, BeautifulSoup4.</li>
	<li>SASS.</li>
	<li>SCRUM.</li>
	<li>Vue.</li>
  <li>Apache, PhpMyAdmin.</li>
	<li>Git.</li>
  
 </ul>
<h4>Демо</h4>
<p>Демо сервиса доступно по адресу: https://lagrange.creativityprojectcenter.ru </p>
<p>Реквизиты тестового пользователя: email: <b>admin@gmail.com</b>, пароль: <b>admin</b></p>




СРЕДА ЗАПУСКА
------------
1) развертывание сервиса производится на Ubuntu 16.04.7 LTS (GNU/Linux 4.4.0-116-generic x86_64)
2) требуется установка интерпретатора python 3.9 и установка пакетов из файла py/requirements.txt
3) требуется установленный web-сервер с поддержкой PHP(версия 7.4+) интерпретации (apache);
4) требуется установленная СУБД MySql (версия 10+);


УСТАНОВКА
------------
### Установка пакета name

Выполните 
~~~
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install name1
sudo apt-get install mariadb-client mariadb-server
git clone https://github.com/Sinclear/default_readme
cd default_readme
...
~~~
### База данных

Необходимо создать пустую базу данных, а подключение к базе прописать в конфигурационный файл сервиса по адресу: папка_сервиса/...
~~~
sudo systemctl restart mariadb
sudo mysql_secure_installation
mysql -u root -p
mypassword
CREATE DATABASE mynewdb;
quit
~~~
### Выполнение миграций

Для заполнения базы данных запустите скрипт lagrange_struct.sql из вашей базы данных

### Установка зависимостей проекта

Установка зависимостей осуществляется с помощью [Composer](http://getcomposer.org/). Если у вас его нет вы можете установить его по инструкции
на [getcomposer.org](http://getcomposer.org/doc/00-intro.md#installation-nix).

После этого выполнить команду в директории проекта:

~~~
composer install
~~~

Для развертывания SPA на Vue выполните следующие команды
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

Установка модулей python осуществляется с помощью пакетного менеджера [pip](https://pypi.org/project/pip/). Если у вас нет пакетного менеджера pip на системе,
вы можете установить его по инструкции, указанной на [pip.pypa.io] https://pip.pypa.io/en/stable/installation/

После выполните команду в директории проекта по пути ./py
~~~
pip install -r requirements.txt
~~~
