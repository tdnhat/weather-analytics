from sqlalchemy import Column, Integer, Float, DateTime
from src.context.database import Base

class Weather(Base):
    __tablename__ = 'weather_data'
    
    id = Column(Integer, primary_key=True)
    temp_c = Column(Float)
    feelslike_c = Column(Float)
    windchill_c = Column(Float)
    heatindex_c = Column(Float)
    dewpoint_c = Column(Float)
    wind_kph = Column(Float)
    wind_degree = Column(Integer)
    pressure_mb = Column(Float)
    precip_mm = Column(Float) 
    humidity = Column(Integer)
    cloud = Column(Integer)
    uv = Column(Float)
    gust_kph = Column(Float)
    last_updated_epoch = Column(Integer)



