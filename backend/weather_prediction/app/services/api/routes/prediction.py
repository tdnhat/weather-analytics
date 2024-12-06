import json
import logging
from datetime import datetime
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app.models.prediction import (
    PredictionWeatherRequest
)
from app.services.prediction_service import WeatherPredictionService

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)  

router = APIRouter(
    prefix='/prediction'
)

@router.post('/weather')
async def get_prediction_weather(request: PredictionWeatherRequest):
    try:
        weather_data = request.weather_data
        prediction_service = WeatherPredictionService()

        prediction_result = prediction_service.predict_tomorrow(data=weather_data)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=prediction_result
        )
    except Exception as e:
        logger.error(f"Error getting prediction weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )