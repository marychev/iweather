To use PostgreSQL in a more isolated way
```
docker volume create postgres-data
docker run -e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -p 5432:5432 --name postgres --mount source=postgres-data,target=/var/lib/postgresql  -d postgres:10
docker exec -it postgres psql -U postgres -h localhost -p 5432 -d iweather
```

Init DB
```
sudo docker exec -it postgres psql -U postgres
CREATE DATABASE iweather;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE iweather TO postgres;
> ```


# Work Api
Example requests to get weather information
```
/weather?city=London&date=2022-02-21
/weather?city=London&country_code=en&date=2022-02-22
```