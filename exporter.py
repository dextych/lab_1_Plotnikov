from datetime import datetime

from sqlalchemy import select

from db_models import SessionLocal, WeatherForecast


def export_to_markdown(city: str, filepath: str = "forecast.md") -> str:
    """
    Выгружает прогноз для указанного города в Markdown-файл.
    Возвращает путь к созданному файлу.
    """
    session = SessionLocal()
    try:
        rows = session.scalars(
            select(WeatherForecast)
            .where(WeatherForecast.city == city)
            .order_by(WeatherForecast.forecast_date)
        ).all()
    finally:
        session.close()

    if not rows:
        raise RuntimeError(f"Нет данных для города {city!r}")

    period_start = rows[0].forecast_date
    period_end = rows[-1].forecast_date

    lines = []
    lines.append("# Прогноз погоды")
    lines.append("")
    lines.append(f"Автоматически определённая локация: {city}  ")
    lines.append(f"Период: {period_start} – {period_end}  ")
    lines.append("")
    lines.append("| Дата       | Мин. темп. (°C) | Макс. темп. (°C) | Описание              | Влажность (%) | Ветер (м/с) |")
    lines.append("|------------|-----------------|------------------|-----------------------|---------------|-------------|")

    for row in rows:
        lines.append(
            f"| {row.forecast_date} "
            f"| {_fmt(row.temp_min)} "
            f"| {_fmt(row.temp_max)} "
            f"| {row.description} "
            f"| {row.humidity} "
            f"| {_fmt(row.wind_speed)} |"
        )

    content = "\n".join(lines) + "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


def _fmt(value: float) -> str:
    #Убирает .0 у целых чисел: 8.0 - 8
    if value == int(value):
        return str(int(value))
    return str(value)