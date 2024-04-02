import json
from connect import connect_to_db
from config import DBNAME, USER, PASSWORD, HOST, PORT, TABLE_NAME_CITY

def fetch_city_list(table_name_city):
    cur, conn = connect_to_db(DBNAME, USER, PASSWORD, HOST, PORT)
    cur.execute("SELECT DISTINCT label, zip_code FROM cities_lat_long{table_name_city}")
    city_list = [{"city_name": row[0].upper(), "zip_code": row[1]} for row in cur.fetchall()]
    conn.close()
    return city_list

def save_city_list_to_json(city_list):
    with open('city_list.json', 'w') as json_file:
        json.dump(city_list, json_file)

if __name__ == "__main__":
    cities = fetch_city_list()
    save_city_list_to_json(cities)


