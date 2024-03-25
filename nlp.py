import requests
import logging
import base64

from config import MY_KEY
from connect import connect_to_db
from config import DBNAME, USER, PASSWORD, HOST, PORT, TABLE_NAME_FC

logger = logging.getLogger(__name__)
cur, conn = connect_to_db(DBNAME, USER, PASSWORD, HOST, PORT)

# Check if my_key is empty or missing
if not MY_KEY or MY_KEY == "":
    print(
        "Your key is not filled or missing. Please provide a key compatible with EdenAI."
    )
    exit(1)

headers = {"Authorization": f"Bearer {MY_KEY}"}


def fetch_forecast_for_city(cur, table_name, city, date, hour=None):
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
        result += "\n".join([f"{column} {value}" for column, value in zip(columns, row)]) + "\n"
    return result.strip()

test = fetch_forecast_for_city(cur, TABLE_NAME_FC, 'montpellier', '2024-03-26', 13)
print(test)

def get_text_from_forecast(cur, table_name, city: str, date: str, hour = None) -> str:
    data = fetch_forecast_for_city(cur, table_name, city, date, hour = None)

    provider = "meta"
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": provider,
        "text": data,
        "chatbot_global_action": f"Act as weather forecast funny guy with the text, remind the {city}, and no matter what, limit your answer to 20 words and do not use any emojis",
        "previous_history": [],
        "temperature": 0.0,
        "max_tokens": 150,
        "fallback_providers": "",
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise error for non-200 responses
        logger.info("Request sent to EdenAI's assistant successfully")
        result = response.json()
        rp = result[provider]
        answer = rp["generated_text"]
        return answer
    except requests.RequestException as e:
        logger.error(f"Failed to fetch response: {e}")
        return ""



def get_speach_from_text(answer: str) -> None:
    url = "https://api.edenai.run/v2/audio/text_to_speech"

    providers = "google"
    language = "en-US"
    payload = {
        "providers": providers,
        "language": language,
        "option": "MALE",
        "text": answer,
        "fallback_providers": ""
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        result = response.json()
        audio_data = result.get('google', {}).get('audio')
        if audio_data:
            audio_bytes = base64.b64decode(audio_data)
            with open("audio.mp3", "wb") as audio_file:
                audio_file.write(audio_bytes)
            print("Audio file downloaded : audio.mp3")
        else:
            print("No audio availible.")
    else:
        print(f"Failed to fetch response : {response.status_code} - {response.text}")


text = get_text_from_forecast(cur, TABLE_NAME_FC, 'montpellier', '2024-03-26', 13)
print(text)

get_speach_from_text(text)



