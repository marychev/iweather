import datetime
import aiohttp
from weather import InfoWeather


class ApiOpenWeather:
    API_KEY = "5f55e90e181d3f051b1c2c94ff81919c"
    URL = f"https://api.openweathermap.org/data/2.5/forecast?appid={API_KEY}"
    weathers = []

    def __init__(self, city: str, date: datetime, country_code: str = ''):
        self.city = city.title()
        self.date = self.validate_date(date)
        self.country_code = country_code.lower()

    @property
    def url(self) -> str:
        url = f"{self.URL}&q={self.city}"
        if not self.country_code:
            return url
        return f"{url},{self.country_code}"

    @classmethod
    def validate_date(cls, value: datetime) -> str:
        value = str(value)
        if f"{InfoWeather.HOURS}:00" not in value and "-" in value:
            return f'{value} {InfoWeather.HOURS}:00:00'
        return value

    async def fetch(self, session) -> list:
        async with session.get(self.url) as response:
            val = []
            try:
                assert response.status == 200
                _json = await response.json()
                val = _json.get('list', [])
            except AssertionError:
                pass
            return val

    async def find(self, session: aiohttp.ClientSession) -> list[InfoWeather]:
        result_list = await self.fetch(session)
        self.weathers = [self.serialize(data) for data in result_list if (self.date in data.get('dt_txt'))]
        return self.weathers

    async def get_all_weathers(self, session: aiohttp.ClientSession) -> list[InfoWeather]:
        result_list = await self.fetch(session)
        self.weathers = [self.serialize(data) for data in result_list]
        return self.weathers

    def serialize(self, data: dict) -> InfoWeather:
        data.update({'city': self.city, 'country_code': self.country_code})
        return InfoWeather(**data)
