import logging
import traceback
import pandas as pd
from datetime import datetime, timedelta
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from src.models.weather_data import Weather
from src.services.external_api_service import ExternalApiService
from src.models.services.weather_prediction_request import (
    WeatherData,
    PredictionWeatherRequest
)
from src.models.services.season_probability_calculate_request import (
    Centroids,
    CalculateSeasonProbabilityRequest
)
from src.context.database import SessionLocal
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

@router.get('/spider-chart')
async def get_spider_chart(
    year: int = Query(..., description="year must be >= 2023")
):
    try:
        db = SessionLocal()

        spider_chart_result = db.query(SeasonalClusteringWeather)\
                                .where(SeasonalClusteringWeather.year == year).first()

        return spider_chart_result
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu spider chart: {str(e)}")
        logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

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

@router.get('/centroids')
async def get_centroids():
    try:
        db = SessionLocal()

        centroids = db.query(SeasonalWeatherCentroid).first()

        print(centroids)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=centroids.to_dict()
        )
    except Exception as e:
        logger.error(f"Error when getting clustering centroids data: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()

@router.get('/season-probability')
async def get_season_probability(
    date: str | None = Query(None, description="Date in YYYY-MM-DD format")
):
    try:
        db = SessionLocal()

        logging.info("Tiến hành lấy dữ liệu nhiệt độ dự đoán")
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
        prediction_response = external_api_service.get_weather_prediction(prediction_request=prediction_request)

        if prediction_response.status_code != 200:
            return JSONResponse(
                status_code=prediction_response.status_code,
                content={"error": f"Lỗi khi dự đoán thời tiết - Unexpected status code: {prediction_response.status_code}"}
            )

        logging.info("Lấy thành công nhiệt độ được dự đoán")
        prediction_response_json = prediction_response.json()
        # Lấy nhiệt độ được dự đoán
        temp_prediction = prediction_response_json.get("predicted_temperature")
        # Lấy centroids
        centroids_db = db.query(SeasonalWeatherCentroid).first()
        centroids = Centroids(
            spring_centroid=centroids_db.spring_centroid,
            summer_centroid=centroids_db.summer_centroid,
            autumn_centroid=centroids_db.autumn_centroid,
            winter_centroid=centroids_db.winter_centroid
        )

        calculation_request = CalculateSeasonProbabilityRequest(
            centroids=centroids,
            temperature=temp_prediction
        )

        calculation_response = external_api_service.get_season_probability(calculation_request=calculation_request)

        if calculation_response.status_code != 200:
            logger.error(f"Lỗi khi tính toán xác suất mùa cho nhiệt độ: {calculation_response.text}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=calculation_response.json()
        )
    
    except Exception as e:
        logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
        logger.error(f"Lỗi khi tính toán xác suất mùa cho nhiệt độ: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
    finally:
        db.close()