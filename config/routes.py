from aiohttp import web

from views import IndexView, InfoView, ClearView


def setup_routes(app: web.Application):
    app.router.add_get('/', IndexView, name='index')
    app.router.add_get('/weather', InfoView, name='weather')
    app.router.add_get('/weather/clear', ClearView, name='weather_clear')
