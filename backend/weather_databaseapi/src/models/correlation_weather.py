from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class CorrelationWeather(Base):
    __tablename__ = "correlation_weathers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
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
    
    def to_dict(self):
        """Converts the model instance to a dictionary."""
        return {
            "id": self.id,
            "year": self.year,
            "temp_humidity_corr": self.temp_humidity_corr,
            "temp_pressure_corr": self.temp_pressure_corr,
            "temp_wind_corr": self.temp_wind_corr,
            "humidity_temp_corr": self.humidity_temp_corr,
            "humidity_pressure_corr": self.humidity_pressure_corr,
            "humidity_wind_corr": self.humidity_wind_corr,
            "pressure_temp_corr": self.pressure_temp_corr,
            "pressure_humidity_corr": self.pressure_humidity_corr,
            "pressure_wind_corr": self.pressure_wind_corr,
            "wind_temp_corr": self.wind_temp_corr,
            "wind_humidity_corr": self.wind_humidity_corr,
            "wind_pressure_corr": self.wind_pressure_corr,
        }