import json
import logging
import datetime
from datetime import datetime
from sqlalchemy import extract
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from src.context.database import SessionLocal
from fastapi import APIRouter, Query, status, Depends
from src.models.centroid_weather import SeasonalWeatherCentroid
from src.models.seasonal_clustering_weather import SeasonalClusteringWeather
from src.dtos.requests.create_seasonal_clustering_dto import CreateSeasonalClustering
from src.dtos.requests.create_centroid_dto import CreateCentroidDto

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)  

router = APIRouter(
    prefix='/clustering'
)

@router.post('/seasonal')
async def create_seasonal_weather(seasonal_weather_dto: CreateSeasonalClustering):
    try:
        db = SessionLocal()

        # Extract the year from the seasonal_weather_dto
        year = seasonal_weather_dto.year
        # Delete existing records with the same year
        db.query(SeasonalClusteringWeather).filter(SeasonalClusteringWeather.year == year).delete()
        
        seasonal_data = SeasonalClusteringWeather(**seasonal_weather_dto.model_dump())
        db.add(seasonal_data)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Seasonal clustering weather data inserted successfully"}
        )
    except Exception as e:
        logger.error(f"Error inserting seasonal clustering weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

@router.post('/centroids')
async def create_centroids(create_centroid_dto: CreateCentroidDto):
    try:
        db = SessionLocal()

        # Delete all existing records
        db.query(SeasonalWeatherCentroid).delete()

        centroid_data = SeasonalWeatherCentroid(**create_centroid_dto.model_dump())
        db.add(centroid_data)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Clustering centroids inserted successfully"}
        )
    except Exception as e:
        logger.error(f"Error inserting clustering centroids data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()