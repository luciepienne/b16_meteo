from meteofrance_api import MeteoFranceClient


def get_fc_from_meteofrance(latitude, longitude):
    meteo = MeteoFranceClient()
    city_forecast = meteo.get_forecast(latitude, longitude)
    data = city_forecast.forecast
    return data
