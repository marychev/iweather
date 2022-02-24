# Install and Run

```
docker-compose up -d --build
## Run
docker-compose up -d
```

### Cервис получения погоды по API
Сервис отвечает информацией о погоде, воспользовавшись [Api OpenWeather](https://openweathermap.org/). 
Выдает информацию о погоде для `Города ` на 12:00 выбранного дня (`2022-02-24`)
Полученная информация сохраняется и при повторном запросе возвращается из Базы Данных.



## Work Api

Example requests to get weather information
* [localhost:8080](http://0.0.0.0:8080/) - All existing weathers in DB
* [localhost:8080/weather?city=NAME&date=Y-M-D](5454) - Find weather

Full example:
* [localhost:8080/weather?city=Ivanovo&code=ru&date=2022-02-28]()
* [localhost:8080/weather?city=London&date=2022-02-28]()

