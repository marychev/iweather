import asyncio
import aiohttp
from aiohttp import web
from postgres import WeatherModel
from weather import InfoWeather, ApiOpenWeather

routes = web.RouteTableDef()


@routes.view("/weather")
class InfoView(web.View):

    @classmethod
    def json_response(cls, result, message: str, extra: str = ''):
        response_data = InfoWeather.response_data(result, message, extra)
        return web.json_response(response_data)

    def get_post_params(self) -> tuple:
        city = self.request.query.get('city')
        country_code = self.request.query.get('country_code')
        date = self.request.query.get('date')
        return city, country_code, date

    def validation(self) -> tuple:
        city, country_code, date = self.get_post_params()
        _date = InfoWeather.parse_date(date)

        if _date and isinstance(_date, dict):
            return False, self.json_response('', _date.get('message'), _date.get('extra'))

        if not city and not _date or city.isdigit():
            err = InfoWeather.error_query_parameters()
            return False, self.json_response('', err.get('message'), err.get('extra'))

        return True, None

    async def get(self):
        city, country_code, date = self.get_post_params()
        parsed_date = InfoWeather.parse_date(date)

        has_valid, json_response = self.validation()
        if not has_valid and json_response:
            return json_response

        weather_model = WeatherModel(self.request, city, country_code, parsed_date)

        data: dict = await weather_model.select()
        if data and 'message' in data.keys():
            return self.json_response(**data)

        open_weather = ApiOpenWeather(city=city, date=date)
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(asyncio.create_task(open_weather.find(session=session)))

        if len(open_weather.weathers) > 0:
            info = open_weather.weathers[0]
            await weather_model.insert(info)
            return self.json_response(info.dumps(), 'ok', 'From API')
        else:
            message = f'Failed to determine the weather for {date} for {city},{country_code}'
            return self.json_response('', message, 'ErrorNotDateInterval')
