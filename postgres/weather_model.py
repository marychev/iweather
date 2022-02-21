import datetime
from aiohttp import web
from sqlalchemy import select, func
from postgres.db import weather
from weather import InfoWeather


class WeatherModel:
    def __init__(self, request: web.Request, city: str, country_code: str, date_dt: datetime):
        self.request = request
        self.city = city
        self.country_code = country_code
        self.date_dt = date_dt

    @classmethod
    async def prepare_pk(cls, connect) -> int:
        _last = await connect.execute(select(weather).order_by(weather.c.id.desc()))
        last = await _last.first()
        return last[0] + 1 if last else 1

    async def select(self):
        async with self.request.app['db'].acquire() as conn:
            result = await conn.execute(select(weather).where(
                weather.c.city == self.city,
                func.DATE(weather.c.date) == self.date_dt.date())
            )

            records = await result.fetchall()

            if len(records) > 1:
                message = f'Manu entries in the database with so parameters: city: {self.city}, country_code: {self.country_code}, date: {self.date_dt}'
                return InfoWeather.response_data(str(records), message)
            elif len(records) == 1:
                info_weather = InfoWeather(**dict(records[0]))
                return info_weather.response_data(info_weather.to_json(), 'ok')

    async def insert(self, info: InfoWeather):
        async with self.request.app['db'].acquire() as conn:
            pk = await self.prepare_pk(conn)
            data = info.__dict__

            data.update({
                "id": pk,
                "date": self.date_dt,
                "wind": info.wind.get('speed', 0.0)
            })

            await conn.execute(weather.insert(), [data])
