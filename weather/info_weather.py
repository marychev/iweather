from datetime import datetime
from typing import Union


class InfoWeather:
    HOURS, MINUTE, SECOND = 12, 0, 0

    def __init__(self, **kwargs):
        self.city = kwargs.get('city', '')
        self.country_code = kwargs.get('country_code', '')
        self.date = kwargs.get('date', None) or kwargs.get('dt_txt', None)
        self.desc = kwargs.get('desc', None) or f"{kwargs['weather'][0]['main']}, {kwargs['weather'][0]['description']}"
        self.temp = kwargs.get('temp', None) or kwargs['main']['temp']
        self.pressure = kwargs.get('pressure', None) or kwargs['main']['pressure']
        self.humidity = kwargs.get('humidity', None) or kwargs['main']['humidity']
        self.wind = kwargs.get('wind', None) or kwargs['wind']['speed']

    def __str__(self):
        return f'Информация о погоде для {self.city} на {self.date}'

    def __repr__(self):
        return f'<InfoWeather: {self.city} {self.country_code} {self.date}>'

    @classmethod
    def response_data(cls, result=None, message: str = 'From DB', extra: str = 'error') -> dict:
        return {
            'result': result,
            'message': message,
            'extra': extra
        }

    @classmethod
    def parse_date(cls, date: str) -> Union[datetime, dict]:
        try:
            y, m, d = [int(d) for d in date.split('-') if d.isdigit()]
            return datetime(y, m, d, cls.HOURS, cls.MINUTE, cls.SECOND)
        except Exception as e:
            return cls.response_data('no', str(e).capitalize(), 'ValueError of date')

    def to_json(self) -> dict:
        data = self.__dict__
        data['date'] = str(data['date'])
        return data

    @staticmethod
    def error_query_parameters() -> dict:
        message = '''You should pass the `city, country_code, date` parameters to get a specific weather info.
        Example query: /weather?city=Ivanovo&country_code&ru$date=2022-02-21'''
        return InfoWeather.response_data('no', message, '[warn]: ErrorQueryParameters')
