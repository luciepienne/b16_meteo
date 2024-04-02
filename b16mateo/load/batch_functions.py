import json

def create_table_cities_lat_long(city_table_name, cur, conn):
    try:
        # Check if the table exists
        cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (city_table_name,))
        table_exists = cur.fetchone()[0]

        if not table_exists:
            # Create table if it does not exist
            cur.execute(
                f"""
                CREATE TABLE {city_table_name} (
                    insee_code VARCHAR(10),
                    city_code VARCHAR(100),
                    zip_code VARCHAR(10),
                    label VARCHAR(100),
                    latitude FLOAT,
                    longitude FLOAT,
                    department_name VARCHAR(100),
                    department_number VARCHAR(10),
                    region_name VARCHAR(100),
                    region_geojson_name VARCHAR(100)
                )
                """
            )

            # Commit the table creation
            conn.commit()
            print(f"Table '{city_table_name}' created successfully!")

            # Read JSON file
            with open("cities_light.json", "r") as fichier:
                data = json.load(fichier)

            for city in data:
                # Check if the city already exists in the database
                cur.execute(
                    f"""
                    SELECT COUNT(*) FROM {city_table_name} WHERE label = %s
                """,
                    (city["label"],),
                )
                count = cur.fetchone()[0]

                # If the city does not exist, insert it into the database
                if count == 0:
                    latitude = float(city["latitude"]) if city["latitude"] else None
                    longitude = float(city["longitude"]) if city["longitude"] else None
                    cur.execute(
                        f"""
                        INSERT INTO {city_table_name} (
                            insee_code, city_code, zip_code, label,
                            latitude, longitude, department_name,
                            department_number, region_name, region_geojson_name
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                        (
                            city["insee_code"],
                            city["city_code"],
                            city["zip_code"],
                            city["label"],
                            latitude,
                            longitude,
                            city["department_name"],
                            city["department_number"],
                            city["region_name"],
                            city["region_geojson_name"],
                        ),
                    )

            # Commit the transaction
            conn.commit()
            print("Data cities transfer to PostgreSQL succeeded!")
        else:
            print(f"Table '{city_table_name}' already exists, skipping table creation.")
    except Exception as e:
        conn.rollback()  # Rollback the transaction if an error occurs
        print(f"Error: {e}")




#get all longitude and latitudes for a given department
def fetch_cities(city_table_name, department_number, cur):
    cur.execute(
        """
        SELECT longitude, latitude, label, department_number
        FROM {}
        WHERE department_number = %s;
        """.format(city_table_name),
        (department_number,),
    )
    cities_data = cur.fetchall()
    return cities_data


# Create the weather table in postgresql if not exists
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

# insert the forecasts for a given city in the table
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
