import sys
import os

# Append the parent directory of your package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from connect import connect_to_db
from batch_functions import (
    create_table_cities_lat_long,
    fetch_cities,
    create_table_weather_fc,
    insert_forecasts,
    delete_old_forecasts_1h,
)
from load_forecast_api import get_fc_from_meteofrance
from prog_bar import print_progress_bar
from config import DBNAME, USER, PASSWORD, HOST, PORT, TABLE_NAME_FC, TABLE_NAME_CITY


# department = ['9', '11', '12', '30', '31', '32', '34']
department = ["34", "30", "11", "12"]
table_name = TABLE_NAME_FC
city_table_name = TABLE_NAME_CITY

cur, conn = connect_to_db(DBNAME, USER, PASSWORD, HOST, PORT)

create_table_cities_lat_long(city_table_name, cur, conn)

create_table_weather_fc(table_name, cur)

for idx, department_number in enumerate(department):
    cities = fetch_cities(city_table_name, department_number, cur)
    print_progress_bar(
        idx + 1,
        len(department),
        prefix=f"Department {idx + 1}/{len(department)}",
        suffix="Complete",
        length=50,
    )

    for city in cities:
        longitude, latitude, label, city_department_number = city
        forecasts = get_fc_from_meteofrance(latitude, longitude)
        insert_forecasts(forecasts, city, table_name, cur, conn)

print("Forecasts transfer to PostgreSQL succeeded!")

delete_old_forecasts_1h(table_name, conn)

cur.close()
conn.close()
