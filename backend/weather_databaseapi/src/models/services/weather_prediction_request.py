from typing import List
from pydantic import BaseModel
from datetime import datetime

class WeatherData(BaseModel):
    time: str
    temp: float
    humidity: float
    pressure: float

class PredictionWeatherRequest(BaseModel):
    model_config = {
        'from_attributes': True,
    }

    weather_data: List[WeatherData]

    def to_dict(self):
        return {
            "weather_data": [data.dict() for data in self.weather_data]
        }