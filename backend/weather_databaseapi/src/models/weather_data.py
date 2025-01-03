from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class Weather(Base):
    __tablename__ = "weather_raw_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_epoch = Column(Integer)
    time = Column(DateTime)
    temp_c = Column(Float)
    temp_f = Column(Float)
    is_day = Column(Integer)
    condition_text = Column(String(100))
    condition_icon = Column(String(200))
    condition_code = Column(Integer)
    wind_mph = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    wind_dir = Column(String(10))
    pressure_mb = Column(Float)
    pressure_in = Column(Float)
    precip_mm = Column(Float)
    precip_in = Column(Float)
    snow_cm = Column(Float)
    humidity = Column(Integer)
    cloud = Column(Integer)
    feelslike_c = Column(Float)
    feelslike_f = Column(Float)
    windchill_c = Column(Float)
    windchill_f = Column(Float)
    heatindex_c = Column(Float)
    heatindex_f = Column(Float)
    dewpoint_c = Column(Float)
    dewpoint_f = Column(Float)
    will_it_rain = Column(Integer)
    chance_of_rain = Column(Integer)
    will_it_snow = Column(Integer)
    chance_of_snow = Column(Integer)
    vis_km = Column(Float)
    vis_miles = Column(Float)
    gust_mph = Column(Float)
    gust_kph = Column(Float)
    uv = Column(Float)