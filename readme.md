# CardHolder

______
Используемые технологии:

- Fast-Api
- PostgresSQL
- SQLAlchemy

____

### Запуск в docker-compose:

- Создаем файл `.env` по примеру [`.env_example`](.env_example)
- Выполняем:

```commandline
docker-compose up --build 
```

обратите внимание что в [docker-compose.yml](docker-compose.yml) настроена миграция и обновление таблиц в БД, это не
очень хорошо, но зато можно сразу запустить приложение, без лишних танцев с бубном
---



### Запуск в docker, без БД:

- Создаем файл `.env` по примеру [`.env_example`](.env_example)
- Выполняем:

### Запуск на локальной машине:

При первом запуске:
Подразумевается что у вас установлена БД PostgresSQL, и запущена

- Создаем файл `.env` по примеру [`.env_example`](.env_example)
- Выполняем:
 ```commandline
sudo su - postgres
```

  Вводим пароль от учетной записи "postgres"

```commandline
 psql
 ```
- Создаем пользователя

```commandline
create user POSTGRES__USER with password 'POSTGRES__PASSWORD';
```
  POSTGRES__USER - заменяем на одноименное значение из `.env`
  
  POSTGRES__PASSWORD - заменяем на одноименное значение из `.env`
- Создаем БД

```commandline
create database POSTGRES__DB;
```
POSTGRES__DB - заменяем на одноименное значение из `.env`
- Назначаем права пользователю которого недавно создали:
```commandline
grant all privileges on all tables in schema public to POSTGRES__USER;
```
- POSTGRES__USER - заменяем на одноименное значение из `.env`
- Выходим:
```commandline
\q
```
```commandline
exit
```
- Переходим в каталог (папку) [backend](backend)

```commandline
cd backend
```
- Устанавливаем миграцию:
```commandline
alembic upgrade head
```
- Запускаем
```commandline
python3 run.py
```  
___

вызов:

- http://localhost:8000/docs - api swagger
- пояснения PORT=`8000` - этот порт задается в `.env` пример в [`.env_example`](.env_example)

_____
