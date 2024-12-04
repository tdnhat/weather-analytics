from typing import Optional
from ..config.logging import logger
from ..config.settings import settings
from app.services.prediction_service import PredictionWeatherService
from app.services.consumers.prediction_consumer import PredictionWeatherConsumer

class WeatherPredictionScheduler:
    _instance: Optional['WeatherPredictionScheduler'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, is_worker: bool = False):
        if not self._initialized:
            logger.info("Khởi tạo WeatherPredictionScheduler")
            self.consumers = {}
            if is_worker:
                self._initialize_consumers()
            self.prediction_service = PredictionWeatherService()
            self._initialized = True
    
    def _initialize_consumers(self):
        """Initialize consumers based on requirements"""
        self.consumers = {
            'prediction': PredictionWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
        }

    async def process_seasonal_clustering(self):
        logger.info("Bắt đầu training dữ liệu")
        try:
            if 'prediction' not in self.consumers:
                self.consumers['prediction'] = PredictionWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            hourly_data = self.consumers['prediction'].get_data()
            # if hourly_data:
            #     result = await self.prediction_service.cluster_daily_data(hourly_data)
            #     if result is not None:
            #         await self.database_api.save_clustering_analysis(result)
            #     logger.info("Hoàn thành phân cụm dữ liệu cho năm")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình training: {str(e)}")
            raise