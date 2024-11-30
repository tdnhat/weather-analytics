from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class SeasonalWeather(Base):
    __tablename__ = "seasonal_weathers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    year = Column(Integer)
    quarter = Column(Integer)
    avg_temp = Column(Float)
    avg_humidity = Column(Float)
    total_precip = Column(Float)
    avg_wind = Column(Float)
    avg_pressure = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "year": self.year,
            "quarter": self.quarter,
            "avg_temp": self.avg_temp,
            "avg_humidity": self.avg_humidity,
            "total_precip": self.total_precip,
            "avg_wind": self.avg_wind,
            "avg_pressure": self.avg_pressure,
            "max_temp": self.max_temp,
            "min_temp": self.min_temp
        }
