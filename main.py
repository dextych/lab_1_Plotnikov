from weather_client import get_forecast, aggregate_forecast
from save_forecast import save_forecast
from exporter import export_to_markdown
from geo_locator import check_ip

def main():
    print("Hell");

if __name__ == "__main__":
    ip = check_ip()
    print(ip)
    data = get_forecast()
    days = aggregate_forecast(data)
    for d in days:
        print(f"{d['date']}:  "
            f"{d['temp_min']}…{d['temp_max']}°C,  "
            f"влажность {d['humidity']}%,  "
            f"ветер до {d['wind_max']} м/с,  "
            f"{d['description']}") 
    city = data["city"]["name"]
    insert, skip = save_forecast(city, days)

    print(f"{city}: вставлено {insert}, пропущено {skip}")
    path = export_to_markdown(city, "forecast.md")
    print(f"Отчёт сохранён: {path}")
