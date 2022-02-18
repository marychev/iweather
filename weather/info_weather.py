import json
import math
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

    @property
    def info(self) -> str:
        return f'''{self}
        Погодные условия:   {self.desc}
        Температура:        {math.floor(self.temp - 273.16)} % ({self.temp} по Кельвину)
        Давление:           {self.pressure} гПа
        Влажность:          {self.humidity} %
        Скорость ветра:     {self.wind} м/с
        '''

    @classmethod
    def parse_date(cls, date: str) -> Union[datetime, dict]:
        _date = None
        try:
            y, m, d = [int(d) for d in date.split('-') if d.isdigit()]
            return datetime(y, m, d, cls.HOURS, cls.MINUTE, cls.SECOND)
        except ValueError as e:
            return {
                'message': str(e).capitalize(),
                'extra': 'ValueError of date'
            }

    @staticmethod
    def error_query_parameters() -> dict:
        message = '''You should pass the `city, country_code, date` parameters to get a specific weather info.
        Example query: /weather?city=Ivanovo&country_code&ru$date=2022-02-21'''
        return {
            'message': message,
            'extra': '[warn]: ErrorQueryParameters::'
        }

    @staticmethod
    def default_converter(obj):
        if isinstance(obj, datetime):
            return obj.__str__()

    def to_json(self):
        data = self.__dict__
        return json.dumps(
            data,
            sort_keys=False,
            indent=4,
            ensure_ascii=False,
            separators=(',', ': '),
            default=self.default_converter,
            allow_nan=True
        )
