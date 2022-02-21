from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
from main import init_app


class IndexApiTestCase(AioHTTPTestCase):
    async def get_application(self) -> web.Application:
        return init_app()

    async def test_success_status(self):
        async with self.client.request("GET", "/") as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()

        self.assertIsInstance(data, dict)
        result = data.get('result')
        self.assertIsInstance(result, list)

    async def test_result_keys_valid(self):
        async with self.client.request("GET", "/") as resp:
            self.assertEqual(resp.status, 200)
            data = await resp.json()

        item = data.get('result')[0]
        self.assertIsInstance(data, dict)

        response_keys = ["city", "country_code", "date", "desc", "temp", "pressure", "humidity", "wind"]
        self.assertEqual(len(response_keys), len(item.keys()))
        self.assertEqual(response_keys, list(item.keys()))
