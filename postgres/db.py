from aiopg.sa import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, Float, String, DateTime

__all__ = ['weather']


meta = MetaData()

weather = Table(
    'weather', meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('city', String(200), nullable=False),
    Column('country_code', String(4), nullable=True),
    Column('date', DateTime, nullable=False),
    Column('desc', String(256), nullable=False),
    Column('temp', Float, nullable=False),
    Column('pressure', Integer, nullable=False),
    Column('humidity', Integer, nullable=False),
    Column('wind', Float, nullable=False)
)


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()

