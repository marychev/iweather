from sqlalchemy import create_engine, MetaData
from config.settings import config
from postgres import db


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[db.weather])


def sample_data(engine):
    conn = engine.connect()

    conn.execute(db.weather.delete())
    conn.execute(db.weather.insert(), [{
        "id": 1,
        "city": "Ivanovo",
        "country_code": "",
        "date": '2022-02-18 12:00:00',
        "desc": "Snow, light snow",
        "temp": 273.57,
        "pressure": 992,
        "humidity": 98,
        "wind": 4.74
    }])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
