from pydantic import BaseModel
from datetime import datetime

class CorrelationWeatherDto(BaseModel):
    model_config = {
        'from_attributes': True,
    }

    year: int
    temp_humidity_corr: float
    temp_pressure_corr: float
    temp_wind_corr: float
    humidity_temp_corr: float
    humidity_pressure_corr: float
    humidity_wind_corr: float
    pressure_temp_corr: float
    pressure_humidity_corr: float
    pressure_wind_corr: float
    wind_temp_corr: float
    wind_humidity_corr: float
    wind_pressure_corr: float