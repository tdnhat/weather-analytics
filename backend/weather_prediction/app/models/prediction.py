from pydantic import BaseModel
from typing import List

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

class WeatherData(BaseModel):
    time: str
    temp: float
    humidity: float
    pressure: float

class PredictionWeatherRequest(BaseModel):
    weather_data: List[WeatherData]
