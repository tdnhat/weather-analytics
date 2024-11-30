from pydantic import BaseModel
from datetime import datetime

class WeatherDateRangeResponseDto(BaseModel):
    model_config = {
        'from_attributes': True,
        'json_encoders': {
            datetime: lambda v: v.isoformat()  # Convert datetime to ISO format string
        }
    }

    id: int
    time_epoch: int
    time: datetime
    temp_c: float
    is_day: int
    wind_kph: float
    humidity: float
    wind_degree: int
    precip_mm: float
    feelslike_c: float
    windchill_c: float
    heatindex_c: float
    dewpoint_c: float
    gust_kph: float
    pressure_mb: float
    pressure_in: float
