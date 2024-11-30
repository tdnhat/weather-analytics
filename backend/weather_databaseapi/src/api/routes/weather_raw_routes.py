import logging
from fastapi import APIRouter, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.context.database import SessionLocal
from src.models.weather_data import Weather
from src.dtos.requests.create_weather_raw_dto import WeatherCreateDto
from src.dtos.requests.weather_daterange_dto import WeatherDateRangeResponseDto
from fastapi import APIRouter, Query, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.schemas.enums import GroupBy
from src.services.weather_service import WeatherService
from src.repositories.weather_repository import WeatherRepository
from src.context.database import get_db


logging.basicConfig(
    level=logging.INFO,
)

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

@router.get('/date-range')
async def get_date_range(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    group_by: GroupBy | None = Query(None, description="Group by 'day', 'week', 'month' or 'none'"),
    db: Session = Depends(get_db)
):
    try:
        repository = WeatherRepository(db)
        service = WeatherService(repository)
        
        result = await service.get_weather_by_date_range(
            start_date,
            end_date,
            group_by
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=result
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )