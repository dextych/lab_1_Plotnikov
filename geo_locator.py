import os 
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY_IP")
base_url = os.getenv("BASE_URL_IP")

if not api_key:
    raise RuntimeError("Ключ не найден")

def check_ip() -> dict:
    headers = {"Authorization": f"Bearer {api_key}"}

    response = requests.get(base_url, headers=headers, timeout=5)

    if response.status_code == 429:
        raise RuntimeError("Превышен лимит запросов к гео-API")

    if response.status_code >= 500:
        raise RuntimeError("Гео-API недоступен")

    response.raise_for_status()
    data = response.json()

    if not data.get("city") or not data.get("loc"):
        raise RuntimeError("Некорректный ответ: нет города или координат")

    lat, lon = data["loc"].split(",")
    data["lat"] = float(lat)
    data["lon"] = float(lon)

    return data