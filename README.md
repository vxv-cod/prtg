## О проекте
...

### Запуск приложения
1. Создать виртуальное окружение и установить зависимости
2. Вызвать в терминале `python3 src/main.py`

### Настройка Alembic для асинхронного драйвера
1. Находясь в корневой директории, запустить  
`alembic init -t async migrations`
2. Перенести папку `migrations` внутрь папки `src`.
3. Заменить `prepend_sys_path` на `. src` и `script_location` на `src/migrations` внутри `alembic.ini`


# Миграции
## Инициализируем alembic
<!-- alembic init migrations -->
alembic init src\migrations
## Корректируем migrations/env.py
### Импортируем в (migrations/env.py) модели вместе с Base (Base = declarative_base())
`from models.user import *`
### и прописываем метаданные в переменную target_metadata
`target_metadata = Base.metadata`
## Создаем ревизию миграции 
```
alembic revision --autogenerate -m "Creat Table"
```
## Обновляем базу данных по номеру последней миграции
```
alembic upgrade 716567e95923
```
```
alembic upgrade 716567e95923
alembic upgrade head
```
## Откатить все миграции
```
alembic downgrade base
```

---
# Запуск и настройка PostgreSQL
0. Переходим в папку: `C:\Program Files\PostgreSQL\16\data`
1.  Первоначально необходимо изменить конфигурационные файлы ***postgresql.conf*** и ***pg_hba.conf*** в директории, куда установлена база данных:
    - **postgresql.conf:**
        *Изменить*
        > listen_addresses = '*'
        Остальные настройки можно оставить по-умолчанию, либо изменить исходя из комплектации сервера
    
    - **pg_hba_conf:**
        *Меняем права на доступ пользователей к базе:*
        - **IPv4 local connections**
        > host all all 0.0.0.0/0 md5

        - **IPv6 local connections**
        > host all all ::0/0 md5
        Это означает, что все пользователи со всех адресов могут подключиться к любой базе данных используя логин и пароль.

2. Сохраняем, перезапускаем службу PostgreSQL
    - Нажимаем комбинацию `Win+R`
    - Вводим `services.msc`
    - Ищем службу `postgres-x64-11` и нажимаем "перезапустить"

3. После этого запускаем меню пуск - `postgresql 11 - SQL bash (psql)` или `SQL Shell (psql)`
    - Все значения по-умолчанию, просто нажимаем enter, вводим пароль для пользователя postgres
    - Создаем базу данных: `create database demo_01;`
    <!-- - Сразу создаем в базе схему **stack**: `create schema stack;` -->
    - Создаем пользователей DataBase_owner и SA, необходимых для работы базы данных и даем им все необходимые права суперюзера:
        ```
        create role DataBase_owner;`
        create role "SA" with password '12345678';
        alter role "SA" superuser;
        alter role "SA" createDataBase;
        alter role "SA" createrole;
        alter role "SA" replication;
        alter role "SA" login;
        ```
    > Аналогично для DataBase_owner (без login)
    > После этого даем всем пользователям права на созданную базу данных
    > ```
    > grant all privileges on database demo_01 to "SA";
    > grant all privileges on database demo_01 to DataBase_owner;
    > ```
---









