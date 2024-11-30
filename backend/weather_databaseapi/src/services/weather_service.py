import json
from datetime import datetime
from typing import Dict, Any
from src.schemas.enums import GroupBy
from src.models.weather_data import Weather
from src.repositories.weather_repository import WeatherRepository
from src.dtos.requests import weather_daterange_dto

class WeatherService:
    def __init__(self, repository: WeatherRepository):
        self.repository = repository

    def format_raw_data(self, row: Weather):
        return weather_daterange_dto.WeatherDateRangeResponseDto.model_validate(row)

    def format_grouped_data(self, group_by: GroupBy, row) -> Dict[str, Any]:
        base_data = {
            "avg_temp_c": float(row.avg_temp_c),
            "avg_wind_kph": float(row.avg_wind_kph),
            "avg_humidity": float(row.avg_humidity),
            "avg_precip_mm": float(row.avg_precip_mm),
            "avg_gust_kph": float(row.avg_gust_kph),
            "avg_feelslike_c": float(row.avg_feelslike_c),
            "avg_windchill_c": float(row.avg_windchill_c),
        }

        if group_by == GroupBy.MONTH:
            return {
                "year": int(row.year),
                "month": int(row.month),
                **base_data
            }
        elif group_by == GroupBy.WEEK:
            return {
                "year": int(row.year),
                "week": int(row.week),
                **base_data
            }
        elif group_by == GroupBy.DAY:
            return {
                "year": int(row.year),
                "month": int(row.month),
                "day": int(row.day),
                **base_data
            }

    async def get_weather_by_date_range(
        self,
        start_date: str,
        end_date: str,
        group_by: GroupBy | None
    ) -> Dict[str, Any]:
        start = datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S")

        if group_by is None:
            raw_data = self.repository.get_by_date_range(start, end)
            formatted_data = [
                self.format_raw_data(row).model_dump() for row in raw_data
            ]
        
            # Convert to JSON-compatible response using custom encoder
            return json.loads(json.dumps({
                "start_date": start_date,
                "end_date": end_date,
                "group_by": None,
                "data": formatted_data
            }, default=str)) 

        query = self.repository.build_group_query(group_by, start, end)
        grouped_data = query.all()

        formatted_data = [
            self.format_grouped_data(group_by, row)
            for row in grouped_data
        ]

        return {
            "start_date": start_date,
            "end_date": end_date,
            "group_by": group_by,
            "data": formatted_data
        }