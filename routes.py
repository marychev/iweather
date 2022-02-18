from aiohttp import web

from views import IndexView, InfoView


def setup_routes(app: web.Application):
    app.router.add_get('/', IndexView, name='index')
    app.router.add_get('/weather', InfoView, name='weather')
