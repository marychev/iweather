import datetime
import aiohttp
from weather import InfoWeather


class ApiOpenWeather:
    API_KEY = "5f55e90e181d3f051b1c2c94ff81919c"
    URL = f"https://api.openweathermap.org/data/2.5/forecast?appid={API_KEY}"
    weathers = []

    def __init__(self, city: str, date: datetime, country_code: str = ''):
        self.city = city
        self._date = self.validate_date(date)
        self.country_code = country_code.lower()

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value: datetime) -> None:
        self._date = self.validate_date(value)

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

    async def fetch(self, session: aiohttp.ClientSession) -> list:
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


# Response:
# 'dt': 1645531200,
# 'main': {
#   'temp': 273.36, 'feels_like': 268.6, 'temp_min': 273.36, 'temp_max': 273.36,
#   'pressure': 1003, 'sea_level': 1003, 'grnd_level': 987, 'humidity': 99, 'temp_kf': 0},
# 'weather': [{'id': 601, 'main': 'Snow', 'description': 'snow', 'icon': '13d'}],
# 'clouds': {'all': 100}, 'wind': {'speed': 4.83, 'deg': 187, 'gust': 11.13},
# 'visibility': 46, 'pop': 1, 'snow': {'3h': 1.7}, 'sys': {'pod': 'd'},
# 'dt_txt': '2022-02-22 12:00:00',
# 'city': 'Ivanovo', 'country_code': 'ru'
