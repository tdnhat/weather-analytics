from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from src.context.database import SessionLocal
from src.models.weather_data import Weather
from src.dtos.requests.create_weather_raw_dto import WeatherCreateDto
import logging

logger = logging.getLogger(__name__)  

router = APIRouter(
    prefix='/weather-raw'
)

@router.post('/insert')
async def create_weather_raw_data(weather_data: list[WeatherCreateDto]):
    try:
        db = SessionLocal()
        
        for data in weather_data:
            weather_raw_data = Weather(**data.model_dump())
            db.add(weather_raw_data)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Weather data inserted successfully"}
        )
    except Exception as e:
        logger.error(f"Error inserting weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()