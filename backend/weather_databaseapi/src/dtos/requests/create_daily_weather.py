from pydantic import BaseModel
from datetime import datetime

class CreateDailyWeatherDto(BaseModel):
    model_config = {
        'from_attributes': True,
        'json_encoders': {
            datetime: lambda v: v.isoformat()  # Convert datetime to ISO format string
        }
    }

    date: str
    avg_temp: float
    avg_humidity: float
    total_precip: float
    avg_wind: float
    avg_pressure: float