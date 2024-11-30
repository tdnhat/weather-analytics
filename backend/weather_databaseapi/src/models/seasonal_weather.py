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
