from connect import connect_to_db
from database import (
    fetch_cities,
    create_table_weather_fc,
    insert_forecasts,
    delete_old_forecasts_1h,
)
from meteo_api import get_fc_from_meteofrance
import sys
import os

# Append the parent directory of your package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from config import DBNAME, USER, PASSWORD, HOST, PORT, TABLE_NAME_FC

department_number = "34"
table_name = TABLE_NAME_FC

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
