from datetime import datetime

# get all needed data on table city


def fetch_cities(department_number, cur):
    cur.execute(
        """
        SELECT longitude, latitude, label, department_number
            FROM cities
            WHERE department_number = %s;
            """,
        (department_number,),
    )
    cities_data = cur.fetchall()
    return cities_data


# Create the weather table if not exists


def create_table_weather_fc(table_name, cur):
    query = """
        CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            department_number INT,
            label_dt_key VARCHAR(100),
            label VARCHAR(100),
            longitude FLOAT,
            latitude FLOAT,                  
            dt TIMESTAMP,
            temperature FLOAT,
            humidity INT,
            sea_level FLOAT,
            wind_speed FLOAT,
            wind_gust FLOAT,
            wind_direction INT,
            weather_icon VARCHAR(10),
            weather_desc VARCHAR(100)
        );
    """.format(
        table_name
    )

    cur.execute(query)


def insert_forecasts(data, city_data, table_name, cur, conn):
    longitude, latitude, label, department_number = city_data
    for item in data:
        dt = item["dt"]
        temperature = item["T"]["value"]
        humidity = item["humidity"]
        sea_level = item["sea_level"]
        wind_speed = item["wind"]["speed"]
        wind_gust = item["wind"]["gust"]
        wind_direction = item["wind"]["direction"]
        weather_icon = item["weather"]["icon"]
        weather_desc = item["weather"]["desc"]

        # Add city name and city_dt_key
        label_dt_key = f"{label}/{dt}"

        cur.execute(
            """
                INSERT INTO {table_name} (longitude, latitude, label, department_number, label_dt_key, dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_icon, weather_desc)
                VALUES (%s, %s, %s, %s, %s, TO_TIMESTAMP(%s), %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """.format(
                table_name=table_name
            ),
            (
                longitude,
                latitude,
                label,
                department_number,
                label_dt_key,
                dt,
                temperature,
                humidity,
                sea_level,
                wind_speed,
                wind_gust,
                wind_direction,
                weather_icon,
                weather_desc,
            ),
        )

        conn.commit()


def delete_old_forecasts_1h(table_name, conn):
    try:
        cur = conn.cursor()

        cur.execute(
            """
            DELETE FROM {}
            WHERE loaded_at < NOW() - INTERVAL '1 hour';
        """.format(
                table_name
            ),
            (table_name,),
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error deleting data older than 1 hour: {e}")
    finally:
        cur.close()
