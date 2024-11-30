from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HourlyWeatherData(BaseModel):
    Id: int
    TimeEpoch: int
    Time: str
    TempC: float
    Humidity: int
    PrecipMm: float
    WindKph: float
    PressureMb: float
    FeelslikeC: float
    WindchillC: float
    HeatindexC: float
    DewpointC: float
    WindDegree: int
    WindDir: str
    

class DailyAnalysis(BaseModel):
    date: str
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float

class SeasonalAnalysis(BaseModel):
    date: str
    year: int
    quarter: int
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float
    max_temp: float
    min_temp: float
    
class CorrelationAnalysis(BaseModel):
    date: str
    temp_humidity_corr:float
    temp_pressure_corr:float
    temp_wind_corr:float
    humidity_temp_corr:float
    humidity_pressure_corr:float
    humidity_wind_corr:float
    pressure_temp_corr:float
    pressure_humidity_corr:float
    pressure_wind_corr:float
    wind_temp_corr:float
    wind_humidity_corr:float
    wind_pressure_corr:float