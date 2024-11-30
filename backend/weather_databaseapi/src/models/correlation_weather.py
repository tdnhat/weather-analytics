from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class CorrelationWeather(Base):
    __tablename__ = "correlation_weathers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    temp_humidity_corr = Column(Float)
    temp_pressure_corr = Column(Float)
    temp_wind_corr = Column(Float)
    humidity_temp_corr = Column(Float)
    humidity_pressure_corr = Column(Float)
    humidity_wind_corr = Column(Float)
    pressure_temp_corr = Column(Float)
    pressure_humidity_corr = Column(Float)
    pressure_wind_corr = Column(Float)
    wind_temp_corr = Column(Float)
    wind_humidity_corr = Column(Float)
    wind_pressure_corr = Column(Float)