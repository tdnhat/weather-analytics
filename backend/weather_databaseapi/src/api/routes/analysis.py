import datetime
import json
from datetime import datetime
import logging
from fastapi.responses import JSONResponse
from sqlalchemy import extract
from src.context.database import SessionLocal
from fastapi import APIRouter, Query, status, Depends
from fastapi.responses import JSONResponse
from src.models.daily_weather import DailyWeather
from src.models.seasonal_weather import SeasonalWeather
from src.models.correlation_weather import CorrelationWeather
from src.dtos.reponses.daily_weather_dto import DailyWeatherDto
from src.dtos.reponses.seasonal_weather_dto import SeasonalWeatherDto
from src.dtos.requests.create_daily_weather import CreateDailyWeatherDto
from src.dtos.reponses.correlation_weather_dto import CorrelationWeatherDto
from src.dtos.requests.create_seasonal_weather_dto import CreateSeasonalWeatherDto
from src.dtos.requests.create_correlation_weather import CreateCorrelationWeatherDto


logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)  

router = APIRouter(
    prefix='/analysis'
)

@router.post('/daily')
async def create_daily_weather(daily_weather_dto: CreateDailyWeatherDto):
    try:
        db = SessionLocal()
        
        monthly_data = DailyWeather(**daily_weather_dto.model_dump())
        db.add(monthly_data)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Daily weather data inserted successfully"}
        )
    except Exception as e:
        logger.error(f"Error inserting daily weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

@router.post('/seasonal')
async def create_seasonal_weather(seasonal_weather_dto: CreateSeasonalWeatherDto):
    try:
        db = SessionLocal()
        
        seasonal_data = SeasonalWeather(**seasonal_weather_dto.model_dump())
        db.add(seasonal_data)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Seasonal weather data inserted successfully"}
        )
    except Exception as e:
        logger.error(f"Error inserting seasonal weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

@router.post('/correlation')
async def create_correlation_weather(correlation_data_weather_dto: CreateCorrelationWeatherDto):
    try:
        db = SessionLocal()

        # Xóa những năm đã tồn tại trước đó
        db.query(CorrelationWeather).filter(CorrelationWeather.year == correlation_data_weather_dto.year).delete()
        
        correlation_data = CorrelationWeather(**correlation_data_weather_dto.model_dump())
        db.add(correlation_data)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Correlation weather data inserted successfully"}
        )
    except Exception as e:
        logger.error(f"Error inserting correlation weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

@router.get('/daily')
async def get_daily_weather(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format")
):
    try:
        db = SessionLocal()

        start = datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S")

        result = db.query(DailyWeather)\
                    .filter(DailyWeather.date.between(start, end))\
                    .all()
        
        # Serialize the result
        serialized_result = [DailyWeatherDto(**daily_weather.to_dict()).model_dump() for daily_weather in result]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {
                "data": serialized_result
            }
        )
    except Exception as e:
        logger.error(f"Error getting daily weather data from {start_date} to {end_date}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()


@router.get('/seasonal')
async def get_seasonal_weather(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    quarter: list[int] = Query([1,2,3,4], description="Quarter(s) of the year (1-4)")
):
    try:
        db = SessionLocal()

        min_start_date = datetime.strptime("2023-11-20", "%Y-%m-%d")
        start = datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S")

        if start < min_start_date:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Start date must be on or after 2023-11-20"}
            )
        
        end = datetime.strptime(f"{end_date} 23:59:59", "%Y-%m-%d %H:%M:%S")

        result = db.query(SeasonalWeather)\
                    .filter(SeasonalWeather.date.between(start, end))\
                    .filter(SeasonalWeather.quarter.in_(quarter))\
                    .all()
        
        # Serialize the result
        serialized_result = [SeasonalWeatherDto(**seasonal_weather.to_dict()).model_dump() for seasonal_weather in result]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {
                "data": serialized_result
            }
        )
    except Exception as e:
        logger.error(f"Error getting seasonal weather data from {start_date} to {end_date} for quarters {quarter}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

@router.get('/correlation')
async def get_correlation_weather(
    year: int = Query(..., description="Year starts from 2023")
):
    try:
        db = SessionLocal()

        # Filter records by year
        result = db.query(CorrelationWeather)\
                    .filter(CorrelationWeather.year == year)\
                    .all()
        
        # Serialize the result
        serialized_result = [CorrelationWeatherDto(**correlation_weather.to_dict()).model_dump() for correlation_weather in result]

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {
                "data": serialized_result
            }
        )

    except Exception as e:
        logger.error(f"Error getting correlation weather data from {year}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()