from sqlalchemy import Column, Integer, String, Float
from src.context.database import Base

class Province(Base):
    __tablename__ = 'provinces'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    region = Column(String(255))
    country = Column(String(255))
    lat = Column(Float)
    lon = Column(Float)
