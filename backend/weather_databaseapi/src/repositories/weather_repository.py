from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import extract, func
from src.models.weather_data import Weather
from src.schemas.enums import GroupBy

class WeatherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_date_range(self, start: datetime, end: datetime):
        return self.db.query(Weather)\
                .filter(Weather.time.between(start, end))\
                .all()

    def build_group_query(self, group_by: GroupBy, start: datetime, end: datetime):
        base_aggregations = [
            func.avg(Weather.temp_c).label('avg_temp_c'),
            func.avg(Weather.wind_kph).label('avg_wind_kph'),
            func.avg(Weather.humidity).label('avg_humidity'),
            func.avg(Weather.precip_mm).label('avg_precip_mm'),
            func.avg(Weather.gust_kph).label('avg_gust_kph'),
            func.avg(Weather.feelslike_c).label('avg_feelslike_c'),
            func.avg(Weather.windchill_c).label('avg_windchill_c'),
        ]

        query_config = {
            GroupBy.MONTH: {
                'groups': [
                    extract('year', Weather.time).label('year'),
                    extract('month', Weather.time).label('month')
                ],
                'order_by': ['year', 'month']
            },
            GroupBy.WEEK: {
                'groups': [
                    extract('year', Weather.time).label('year'),
                    extract('week', Weather.time).label('week')
                ],
                'order_by': ['year', 'week']
            },
            GroupBy.DAY: {
                'groups': [
                    extract('year', Weather.time).label('year'),
                    extract('month', Weather.time).label('month'),
                    extract('day', Weather.time).label('day'),
                ],
                'order_by': ['year', 'month', 'day']
            }
        }

        config = query_config[group_by]
        return self.db.query(
            *config['groups'],
            *base_aggregations
        ).filter(
            Weather.time.between(start, end)
        ).group_by(
            *config['groups']
        ).order_by(
            *config['order_by']
        )