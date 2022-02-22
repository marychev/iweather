from aiohttp import web
from postgres import db
from views import IndexView

routes = web.RouteTableDef()


@routes.view("/weather/clear")
class ClearView(IndexView):

    async def get(self):
        async with self.request.app['db'].acquire() as conn:
            await conn.execute(db.weather.delete())
        return await super(ClearView, self).get()
