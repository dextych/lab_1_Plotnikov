from geo_locator import check_ip
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from statistics import mean
from collections import Counter, defaultdict

load_dotenv()
weather_key = os.getenv("API_KEY_WEATHER")
url_weather = os.getenv("BASE_URL_WEATHER")
days = 4

if not weather_key:
    raise RuntimeError("Ключ погоды не найден")

def get_forecast() -> dict:
    data_ip = check_ip()

    params = {
        "lat": data_ip["lat"],
        "lon": data_ip["lon"],
        "appid": weather_key,
        "units": "metric",
        "lang": "ru",
    }

    response = requests.get(url_weather, params=params, timeout=5)

    if response.status_code == 401:
        raise RuntimeError("Неверный ключ OpenWeatherMap")

    if response.status_code == 429:
        raise RuntimeError("Превышен лимит запросов к OpenWeatherMap")

    if response.status_code >= 500:
        raise RuntimeError("OpenWeatherMap недоступен")

    response.raise_for_status()

    data = response.json()

    return data


def aggregate_forecast(data: dict) -> list[dict]:
    # Раскладываем точки по дням
    days_map = defaultdict(list)

    for item in data["list"]:
        dt = datetime.fromisoformat(item["dt_txt"]) 
        day = dt.date()                              
        days_map[day].append(item)

    # Считаем статистику для каждого дня
    result = []

    for day in sorted(days_map):
        items = days_map[day]

        temp_min = min(i["main"]["temp_min"] for i in items)
        temp_max = max(i["main"]["temp_max"] for i in items)

        humidity = mean(i["main"]["humidity"] for i in items)
        wind_max = max(i["wind"]["speed"] for i in items)

        description = _pick_description(items)

        result.append({
            "date": day.isoformat(),
            "temp_min": round(temp_min, 1),
            "temp_max": round(temp_max, 1),
            "humidity": round(humidity, 1),
            "wind_max": round(wind_max, 1),
            "description": description,
        })

    return result[:days]


def _pick_description(items: list[dict]) -> str:
    #Берёт описание из полуденной точки, а если её нет — самое частое
    for item in items:
        hour = datetime.fromisoformat(item["dt_txt"]).hour
        if 11 <= hour <= 14:
            return item["weather"][0]["description"]

    # Иначе самое частое описание за день
    descriptions = [i["weather"][0]["description"] for i in items]
    return Counter(descriptions).most_common(1)[0][0]