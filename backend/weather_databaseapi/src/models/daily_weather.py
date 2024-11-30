from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class DailyWeather(Base):
    __tablename__ = "daily_weathers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    avg_temp = Column(Float)
    avg_humidity = Column(Float)
    total_precip = Column(Float)
    avg_wind = Column(Float)
    avg_pressure = Column(Float)

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "avg_temp": self.avg_temp,
            "avg_humidity": self.avg_humidity,
            "total_precip": self.total_precip,
            "avg_wind": self.avg_wind,
            "avg_pressure": self.avg_pressure
        }