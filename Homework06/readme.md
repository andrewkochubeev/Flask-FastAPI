# Интернет-магазин с использованием базы данных sqlite
## Описание

Интернет-магазин, использующий базу данных sqlite и фреймворк FastAPI python интерпретатора.
База данных состоит из трех таблиц: товары, заказы и пользователи.


* Таблица «Товары» содержит информацию о доступных товарах, их описаниях и ценах.

    Поля таблицы:
    * id (первичный ключ)
    * Название
    * Описание
    * Цена
* Таблица «Заказы» содержит информацию о заказах, сделанных пользователями.

    Поля таблицы:
    * id (первичный ключ)
    * id пользователя (внешний ключ)
    * id товара (внешний ключ)
    * Дата заказа
    * Статус заказа
* Таблица «Пользователи» содержит информацию о зарегистрированных пользователях магазина.

    Поля таблицы:
    * id (первичный ключ)
    * Имя
    * Фамилия
    * Адрес электронной почты
    * Пароль

## Запуск программы

Запуск программы осуществляется через файл main.py IDE PyCharm или подобных, либо через командную строку с помощью команды `python main.py`

## Управление содержимым

Управление содержимым происходит с помощью GET, POST, PUT, DELETE запросов
* Чтобы создать одну запись в таблице, необходимо отправить POST-запрос по URL: *host/*table/
* Чтобы вывести все записи в таблице, необходимо отправить GET-запрос по URL: *host/*table/
* Чтобы вывести одну запись в таблице по id, необходимо отправить GET-запрос по URL: *host/*table/*id
* Чтобы изменить одну запись в таблице по id, необходимо отправить PUT-запрос по URL: *host/*table/*id
* Чтобы удалить одну запись в таблице по id, необходимо отправить DELETE-запрос по URL: *host/*table/*id

*host - адрес сервера, на котором запущена программа

*table - название таблицы (products, users или orders)

*id - идентификатор записи таблицы

## Зависимости

Все необходимые зависимости указаны в файле requirements.txt