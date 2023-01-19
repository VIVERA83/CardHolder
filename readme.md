Зупуск

```commandline
docker-compose up --build 
```

Либо можно отдельно запустить [dockerfile_backend](dockerfile_backend) без БД, приложение
не сможет возвращать и принимать данные. 

```commandline
docker build -f dockerfile_backend -t cardholder . && docker run -it -p 8000:8000 -e POSTGRES__DB=user_db -e POSTGRES__USER=user -e POSTGRES__PASSWORD=user_pass  --rm --name ca cardholder 
```


