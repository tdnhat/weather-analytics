from typing import Optional
from ..config.logging import logger
from ..config.settings import settings
from app.services.prediction_service import WeatherPredictionService
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
            self.prediction_service = WeatherPredictionService()
            self._initialized = True
    
    def _initialize_consumers(self):
        """Initialize consumers based on requirements"""
        self.consumers = {
            'training_prediction_model': PredictionWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
        }

    async def process_training_model(self):
        logger.info("Bắt đầu training dữ liệu")
        try:
            if 'training_prediction_model' not in self.consumers:
                self.consumers['training_prediction_model'] = PredictionWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            hourly_data = self.consumers['training_prediction_model'].get_data()
            if hourly_data:
                result = await self.prediction_service.training_model(hourly_data)
                if result is not None:
                    logger.info(f"Training dữ liệu thành công {result}")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình training: {str(e)}")
            raise