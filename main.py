from aiohttp import web

from settings import config
from routes import setup_routes
from postgres import db

app = web.Application()
app['config'] = config

setup_routes(app)
app.cleanup_ctx.append(db.pg_context)
web.run_app(app)
