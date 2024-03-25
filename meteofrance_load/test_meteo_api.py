import pytest
from b16_meteo.github.meteofrance_load.meteo_api import get_fc_from_meteofrance


def test_meteo_api():
    lat = 43.450990329
    long = 3.274991171

    # data[0]
    # {'dt': 1711108800,
    # 'T': {'value': 24.6, 'windchill': 25.2},
    # 'humidity': 35,
    # 'sea_level': 1020.3,
    # 'wind': {'speed': 2, 'gust': 0, 'direction': 130, 'icon': 'SE'},
    # 'rain': {'1h': 0}, 'snow': {'1h': 0}, 'iso0': 3450,
    # 'rain snow limit': 'Non pertinent', 'clouds': 10,
    # 'weather': {'icon': 'p1j', 'desc': 'Ensoleillé'}},

    data = get_fc_from_meteofrance(lat, long)
    print(data)
    # Check if the data returned is as expected
    assert data != None
    assert isinstance(data, list), "Returned data should be a list"
    assert len(data) >= 73, "returned data should be up to 73"
    assert data[0]["dt"] >= 171000000, "Unexpected dt value in the first forecast entry"
    assert (
        data[0]["humidity"] >= 20
    ), "Unexpected humidity value in the first forecast entry"
    assert (
        data[0]["T"]["value"] <= 50.0
    ), "Unexpected temperature value in the first forecast entry"
    assert "rain" in data[0]


test_meteo_api()
