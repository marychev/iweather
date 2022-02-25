# IWeather: Cервис получения погоды по API
Сервис отвечает информацией о погоде, воспользовавшись [Api OpenWeather](https://openweathermap.org/). 
Выдает информацию о погоде для `Города ` на 12:00 выбранного дня (`2022-02-24`)
Полученная информация сохраняется и при повторном запросе возвращается из Базы Данных.


## Установка и запуск
```
docker-compose up -d --build
```


## Work Api

Примеры GET запросов для получения погоды

* [localhost:8080](http://0.0.0.0:8080/) - All existing weathers in DB
* [localhost:8080/weather?city=NAME&date=Y-M-D](http://0.0.0.0:8080/weather?city=London&date=2022-03-01) - Find weather
* [localhost:8080/weather/clear](http://0.0.0.0:8080/weather/clear) - Clear all weathers

Полный пример запроса:
* [localhost:8080/weather?city=Ivanovo&country_code=ru&date=2022-03-01](http://0.0.0.0:8080/weather?city=Ivanovo&country_code=ru&date=2022-03-01)
* [localhost:8080/weather?city=London&date=2022-03-01](http://0.0.0.0:8080/weather?city=London&date=2022-03-01)



### Help
```
# Run app
docker-compose up -d

# Run tests
docker exec -it iweather bash
root@e38077e0fa24:/code# pytest 

# Stop local postgres
sudo service postgresql stop
```
 
> Внимание: Так как используется демо версия Api Open weather доступный период 5 дней от текущей даты.\
> В обратном случае будет выведено предупреждение об этом.
