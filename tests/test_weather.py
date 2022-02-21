from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
from main import init_app


class WeatherApiTestCase(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        return init_app()

    async def test_success_result(self):
        async with self.client.request("GET", "/weather?city=Ivanovo&date=2022-02-22") as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()

        self.assertIsInstance(data, dict)
        result = data.get('result')
        self.assertIsInstance(result, dict)
