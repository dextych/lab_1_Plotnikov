from weather_client import get_forecast, aggregate_forecast
from save_forecast import save_forecast
from exporter import export_to_markdown

def main():
    print("Hell");

if __name__ == "__main__":
    data = get_forecast()
    days = aggregate_forecast(data) 
    city = data["city"]["name"]
    # insert, skip = save_forecast(city, days)

    # print(f"{city}: вставлено {insert}, пропущено {skip}")
    path = export_to_markdown(city, "forecast.md")
    print(f"Отчёт сохранён: {path}")
