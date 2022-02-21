import datetime
import aiohttp
from weather import InfoWeather


class ApiOpenWeather:
    API_KEY = "5f55e90e181d3f051b1c2c94ff81919c"
    URL = f"https://api.openweathermap.org/data/2.5/forecast?appid={API_KEY}"
    weathers = []

    def __init__(self, city, country_code='', date=''):
        self.city = city
        self.country_code = country_code.lower()
        self._date = self.validate_date(date)

    @property
    def date(self) -> str:
        return self._date

    @date.setter
    def date(self, value) -> None:
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

    async def find(self, session: aiohttp.ClientSession) -> list[InfoWeather]:
        async with session.get(self.url) as response:
            try:
                assert response.status == 200
                _json = await response.json()

                for key, val in _json.items():
                    if key == 'cod' and int(val) != 200:
                        raise Exception(f"Code has not 200: {key}: {val}")

                    if key == 'list' and isinstance(val, list):
                        self.weathers = [self.serialize(data) for data in val if (self.date in data.get('dt_txt'))]

                return self.weathers
            except AssertionError as e:
                pass

    async def get_all_weathers(self, session: aiohttp.ClientSession) -> list[InfoWeather]:
        async with session.get(self.url) as response:
            assert response.status == 200
            _json = await response.json()

            for key, val in _json.items():
                if key == 'cod' and int(val) != 200:
                    raise Exception(f"Code has not 200: {key}: {val}")

                if key == 'list' and isinstance(val, list):
                    self.weathers = [self.serialize(data) for data in val]

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
