import logging
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from src.context.database import SessionLocal
from fastapi import APIRouter, Query, status, Depends
from fastapi.responses import JSONResponse
from src.models.daily_weather import DailyWeather
from src.models.seasonal_weather import SeasonalWeather
from src.models.correlation_weather import CorrelationWeather
from src.dtos.requests.create_daily_weather import CreateDailyWeatherDto
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
