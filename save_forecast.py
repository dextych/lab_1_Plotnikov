from datetime import datetime

from sqlalchemy.dialects.sqlite import insert

from db_models import SessionLocal, WeatherForecast


def save_forecast(city: str, days: list[dict]) -> tuple[int, int]:
    #Вставляет прогноз, игнорируя дубликаты по паре (city, forecast_date).
    session = SessionLocal()
    inserted = 0
    skipped = 0
    try:
        for d in days:
            stmt = (
                insert(WeatherForecast)
                .values(
                    city=city,
                    forecast_date=datetime.fromisoformat(d["date"]).date(),
                    temp_min=d["temp_min"],
                    temp_max=d["temp_max"],
                    humidity=int(d["humidity"]),
                    wind_speed=d["wind_max"],
                    description=d["description"],
                )
                .on_conflict_do_nothing(index_elements=["city", "forecast_date"])
            )
            result = session.execute(stmt)
            if result.rowcount:
                inserted += 1
            else:
                skipped += 1

        session.commit()
        return inserted, skipped
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()