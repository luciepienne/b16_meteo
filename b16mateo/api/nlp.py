import requests
import logging
import base64
import sys
import os


# Append the parent directory of your package to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from connect import connect_to_db
from config import DBNAME, USER, PASSWORD, HOST, PORT, TABLE_NAME_FC, MY_KEY


logger = logging.getLogger(__name__)
cur, conn = connect_to_db(DBNAME, USER, PASSWORD, HOST, PORT)
table_name = TABLE_NAME_FC

# Check if my_key is empty or missing
if not MY_KEY or MY_KEY == "":
    print(
        "Your key is not filled or missing. Please provide a key compatible with EdenAI."
    )
    exit(1)

headers = {"Authorization": f"Bearer {MY_KEY}"}


def fetch_forecast_for_city(city, date, hour=None):

    if hour is None:
        timestamp = date
        query = f"""
        SELECT dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_desc
            FROM {table_name}
            WHERE label = %s AND date_trunc('day', dt) = %s
        """
        cur.execute(query, (city, timestamp))
    else:
        timestamp = f"{date} {hour:02}:00:00.000"
        cur.execute(
            f"""
            SELECT dt, temperature, humidity, sea_level, wind_speed, wind_gust, wind_direction, weather_desc
                FROM {table_name}
                WHERE label = %s AND dt = %s
            """,
            (city, timestamp),
        )
    columns = [
        "Forecast date and hour",
        "Temperature",
        "Humidity",
        "Sea Level",
        "Wind Speed",
        "Wind Gust",
        "Wind Direction",
        "Weather Description",
    ]
    cities_data = cur.fetchall()
    result = ""
    for row in cities_data:
        result += (
            "\n".join([f"{column} {value}" for column, value in zip(columns, row)])
            + "\n"
        )
    return result.strip()


def get_text_from_forecast(city: str, date: str, hour=None) -> str:
    data = fetch_forecast_for_city(city, date, hour=None)

    provider = "meta"
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": provider,
        "text": data,
        "chatbot_global_action": f"Act as weather forecast guy, remind the {city}",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": "",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        logger.info("Request sent to EdenAI's assistant successfully")
        result = response.json()
        rp = result[provider]
        answer = rp["generated_text"]
        return answer
    except requests.RequestException as e:
        logger.error(f"Failed to fetch response: {e}")
        return ""


def get_speach_from_text(answer: str, city: str, date: str, hour=None):

    url = "https://api.edenai.run/v2/audio/text_to_speech"
    providers = "google"
    language = "en-US"
    payload = {
        "providers": providers,
        "language": language,
        "option": "MALE",
        "text": answer,
        "fallback_providers": "",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        audio_data = result.get("google", {}).get("audio")
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            if hour is None:
                filename = f"audio_{city}_{date}.mp3"
            else:
                filename = f"audio_{city}_{date}_{hour}.mp3"
            print(f"filename: {filename}")
            # storage_dir = "../forecast_storage/audio"
            # if not os.path.exists(storage_dir):
            #     os.makedirs(storage_dir)

            # with open(os.path.join(storage_dir, filename), "wb") as audio_file:
            with open(f"audio/{filename}", "wb") as audio_file:
                audio_file.write(audio_bytes)
            print(f"Audio file downloaded: {filename}")
            return filename
        else:
            print("No audio availible.")
    else:
        print(f"Failed to fetch response : {response.status_code} - {response.text}")


# text = get_text_from_forecast("moulis", "2024-03-29", 13)
# print(text)
# text = "C'est l'été, mais pas trop chaud, ici à Montpellier. Pluies éparses tout au long de la journée. Il est recommandé de se munir d'un parapluie et de vêtements chauds pour sortir."
# get_speach_from_text(text, "moulis", "2024-03-29", 13)
