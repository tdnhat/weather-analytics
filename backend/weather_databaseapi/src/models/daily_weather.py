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
