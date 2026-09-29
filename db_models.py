from datetime import datetime, date
from dotenv import load_dotenv
import os
from sqlalchemy import String, Float, Integer, Date, DateTime, func, create_engine, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

load_dotenv()
url_db = os.getenv("DATABASE_URL")
class Base(DeclarativeBase): #пустой класс
    pass


#модель
class WeatherForecast(Base):
    __tablename__ = "weather_forecast"
    __table_args__ = (
        UniqueConstraint("city", "forecast_date", name="uq_city_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    temp_min: Mapped[float] = mapped_column(Float, nullable=False)
    temp_max: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[int] = mapped_column(Integer, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"<WeatherForecast(city={self.city!r}, "
            f"date={self.forecast_date}, "
            f"{self.temp_min}…{self.temp_max}°C)>"
        )


# подключение и создание таблицы

engine = create_engine(url_db, echo=False)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)