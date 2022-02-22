from datetime import datetime
from urllib.parse import urlparse
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase
from main import init_app
from postgres import WeatherModel
from weather import InfoWeather, ApiOpenWeather


class WeatherApiTestCase(AioHTTPTestCase):
    today = datetime.today().date()
    dt = datetime(year=today.year, month=today.month, day=today.day+1).date()
    CITY = 'Ivanovo'
    DATE = dt.strftime("%Y-%m-%d")
    URL = f"/weather?city={CITY}&date={DATE}"

    async def get_application(self) -> web.Application:
        return init_app()

    async def test_success_result_without_country_code(self):
        async with self.client.request("GET", self.URL) as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()

        self.assertIsInstance(data, dict)
        result = data.get('result')
        self.assertIsInstance(result, dict)

    async def test_success_result_with_country_code(self):
        async with self.client.request("GET", f"{self.URL}&country_code=ru") as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()

        self.assertIsInstance(data, dict)
        result = data.get('result')
        self.assertIsInstance(result, dict)

    async def test_keep_to_db_and_return_api_result(self):
        city = 'London'

        async with self.client.request("GET", f"/weather?city={city}&date={self.DATE}") as resp:
            resp.app = self.app
            query_string = urlparse(str(resp.url)).query
            date = InfoWeather.parse_date(self.DATE)

            self.assertIn(city, query_string)
            self.assertIn(self.DATE, query_string)

            weather_model = WeatherModel(request=resp, city=city, date_dt=date, country_code='')
            qs = await weather_model.select()

            qs_result = qs.get('result')
            instance = InfoWeather(**qs_result)

            self.assertEqual(instance.to_json(), qs_result)
            self.assertEqual(instance.city, city)
            self.assertEqual(instance.city, qs_result['city'])

            self.assertEqual(ApiOpenWeather.validate_date(date), qs_result['date'])
            self.assertEqual(instance.date.replace(" 12:00:00", ""), self.DATE)
            self.assertEqual(instance.date, qs_result['date'])

            self.assertEqual(instance.country_code, qs_result['country_code'])
            self.assertEqual(instance.desc, qs_result['desc'])
            self.assertEqual(instance.temp, qs_result['temp'])
            self.assertEqual(instance.pressure, qs_result['pressure'])
            self.assertEqual(instance.humidity, qs_result['humidity'])
            self.assertEqual(instance.wind, qs_result['wind'])
