import json
import traceback
import logging
import pandas as pd
from sqlalchemy import extract
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from src.context.database import SessionLocal
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from src.services.external_api_service import ExternalApiService
from src.models.daily_weather import DailyWeather
from src.models.weather_data import Weather
from src.models.services.weather_prediction_request import (
    WeatherData,
    PredictionWeatherRequest
)

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)  

router = APIRouter(
    prefix='/prediction'
)

@router.get('/tomorrow')
async def get_tommorow_predict_weather(
    date: str | None = Query(None, description="Prediction date in YYYY-MM-DD format")
):
    try:
        db = SessionLocal()

        predict_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if date is not None:
            predict_date = datetime.strptime(f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S")

        seven_days_ago = predict_date - timedelta(days=7)

        previous_dates = db.query(Weather)\
                            .filter(Weather.time >= seven_days_ago, Weather.time < predict_date)\
                            .all()
        
         # Convert list of Weather objects to list of dictionaries
        weather_data_list = []
        for entry in previous_dates:
            data = WeatherData(
                time=entry.time.isoformat(),
                temp=entry.temp_c,
                humidity=entry.humidity,
                pressure=entry.pressure_mb
            )
            weather_data_list.append(data)

        # Create a pandas DataFrame from the list of dictionaries
        df = pd.DataFrame([vars(d) for d in weather_data_list])
        df['time'] = pd.to_datetime(df['time'])
        df.set_index('time', inplace=True)

        daily_data = df.resample('D').agg({
            'temp': 'mean',
            'humidity': 'mean',
            'pressure': 'mean'
        })

        daily_data.columns = ['temp', 'humidity', 'pressure']

        daily_data = daily_data.reset_index()

        daily_data['time'] = daily_data['time'].dt.strftime("%Y-%m-%d")

        prediction_request = PredictionWeatherRequest(
            weather_data=[WeatherData(**row) for index, row in daily_data.iterrows()]
        )

        # Tiến hành lấy giá trị dự đoán thời tiết
        external_api_service = ExternalApiService()
        response = external_api_service.get_weather_prediction(prediction_request=prediction_request)

        # Check the response status code
        if response.status_code == 200:
            logger.info("Lấy dữ liệu dự đoán thời tiết thành công")
            
            return JSONResponse(
                status_code=response.status_code,
                content=response.json()
            )
        else:
            logger.error(f"Lỗi khi dự đoán thời tiết - Unexpected status code: {response.status_code}")
            logger.error(f"Lỗi khi dự đoán thời tiết -  Response content: {response.text}")

            return JSONResponse(
                status_code=response.status_code,
                content={"error": f"Lỗi khi dự đoán thời tiết - Unexpected status code: {response.status_code}"}
            )
    
    except Exception as e:
        logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
        logger.error(f"Error getting prediction weather data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )