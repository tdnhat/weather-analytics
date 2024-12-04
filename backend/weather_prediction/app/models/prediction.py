from ast import Dict
from re import I
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