from aiohttp import web
from postgres import db
from weather import InfoWeather

routes = web.RouteTableDef()


@routes.view("/")
class IndexView(web.View):
    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            cursor = await conn.execute(db.weather.select())
            records = await cursor.fetchall()
            result = [InfoWeather(**dict(q)).__dict__ for q in records]

            return web.json_response({
                'result': str(result),
            })
