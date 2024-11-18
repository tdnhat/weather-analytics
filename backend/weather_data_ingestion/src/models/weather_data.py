from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Weather(BaseModel):
    time_epoch: Optional[int] = None
    time: Optional[datetime] = None
    temp_c: Optional[float] = None
    temp_f: Optional[float] = None
    is_day: Optional[int] = None
    condition_text: Optional[str] = None
    condition_icon: Optional[str] = None
    condition_code: Optional[int] = None
    wind_mph: Optional[float] = None
    wind_kph: Optional[float] = None
    wind_degree: Optional[int] = None
    wind_dir: Optional[str] = None
    pressure_mb: Optional[float] = None
    pressure_in: Optional[float] = None
    precip_mm: Optional[float] = None
    precip_in: Optional[float] = None
    snow_cm: Optional[float] = None
    humidity: Optional[int] = None
    cloud: Optional[int] = None
    feelslike_c: Optional[float] = None
    feelslike_f: Optional[float] = None
    windchill_c: Optional[float] = None
    windchill_f: Optional[float] = None
    heatindex_c: Optional[float] = None
    heatindex_f: Optional[float] = None
    dewpoint_c: Optional[float] = None
    dewpoint_f: Optional[float] = None
    will_it_rain: Optional[int] = None
    chance_of_rain: Optional[int] = None
    will_it_snow: Optional[int] = None
    chance_of_snow: Optional[int] = None
    vis_km: Optional[float] = None
    vis_miles: Optional[float] = None
    gust_mph: Optional[float] = None
    gust_kph: Optional[float] = None
    uv: Optional[float] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }