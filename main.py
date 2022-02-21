from aiohttp import web

from config.settings import config
from config.routes import setup_routes
from postgres import db


def init_app() -> web.Application:
    app = web.Application()
    app['config'] = config

    setup_routes(app)
    app.cleanup_ctx.append(db.pg_context)
    return app


if __name__ == '__main__':
    app = init_app()
    web.run_app(app)
