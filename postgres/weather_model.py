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

    @property
    def response_data(self) -> dict:
        return {
            'result': '',
            'extra': 'From DB',
            'message': 'error'}

    @classmethod
    async def prepare_pk(cls, connect) -> int:
        _last = await connect.execute(select(weather).order_by(weather.c.id.desc()))
        last = await _last.first()
        pk = last[0] + 1
        return pk

    async def select(self):
        async with self.request.app['db'].acquire() as conn:
            result = await conn.execute(select(weather).where(
                weather.c.city == self.city,
                func.DATE(weather.c.date) == self.date_dt.date())
            )

            records = await result.fetchall()
            response_data = self.response_data

            if len(records) > 1:
                response_data.update({
                    'result': str(records),
                    'message': f'Manu entries in the database with so parameters: city: {self.city}, country_code: {self.country_code}, date: {self.date_dt}'
                })
                return response_data
            elif len(records) == 1:
                data = dict(records[0])
                info_weather = InfoWeather(**data)

                response_data.update({
                    'result': info_weather.to_json(),
                    'message': 'ok',
                })
                return response_data

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
