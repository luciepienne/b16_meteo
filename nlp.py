import requests
import logging
from config import MY_KEY
import base64

logger = logging.getLogger(__name__)

# Check if my_key is empty or missing
if not MY_KEY or MY_KEY == "":
    print(
        "Your key is not filled or missing. Please provide a key compatible with EdenAI."
    )
    exit(1)


headers = {"Authorization": f"Bearer {MY_KEY}"}

def get_text_from_forecast() -> str:
    data = """
    {
    'dt': 1711108800, 
    'T': {'value': 24.6, 'windchill': 25.2}, 
    'humidity': 35, 
    'sea_level': 1020.3, 
    'wind': {'speed': 2, 'gust': 0, 'direction': 130, 'icon': 'SE'}, 
    'rain': {'1h': 10}, 'snow': {'1h': 10}, 'iso0': 3450, 
    'rain snow limit': 'Non pertinent', 'clouds': 80, 
    'weather': {'icon': 'p1j', 'desc': 'Ensoleillé'}
    }
    """

    provider = "meta"
    url = "https://api.edenai.run/v2/text/chat"
    payload = {
        "providers": provider,
        "text": data,
        "chatbot_global_action": f"Act as weather forecast funny guy with the text, limit your answer to 20 words and no emojis",
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
        


def get_speach_from_text(answer: str) -> None:
    url = "https://api.edenai.run/v2/audio/text_to_speech"

    providers = "google"
    language = "fr-FR"
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


text = get_text_from_forecast()
print(text)

get_speach_from_text(text)



