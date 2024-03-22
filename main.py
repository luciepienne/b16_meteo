from connect import connect_to_db
from database import (
    fetch_cities,
    create_table_weather_fc,
    insert_forecasts,
    delete_old_forecasts_1h,
)
from meteo_api import get_fc_from_meteofrance

from config import DBNAME, USER, PASSWORD, HOST, PORT

department_number = '34'
table_name = "forecast_weather"

cur, conn = connect_to_db(DBNAME, USER, PASSWORD, HOST, PORT)

create_table_weather_fc(table_name, cur)

cities = fetch_cities(department_number, cur)

for city in cities:
    longitude, latitude, label, department_number = city
    forecasts = get_fc_from_meteofrance(latitude, longitude)
    insert_forecasts(forecasts, city, table_name, cur, conn)

print("Forecasts transfer to PostgreSQL succeeded!")

delete_old_forecasts_1h(table_name, conn)

cur.close()
conn.close()
