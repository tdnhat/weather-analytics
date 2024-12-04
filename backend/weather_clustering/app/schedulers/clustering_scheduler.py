from typing import Optional
from ..config.logging import logger
from ..config.settings import settings
from ..services.database_api import DatabaseApiService
from app.services.clustering_service import ClusteringWeatherService
from app.services.consumers.clustering_consumer import ClusteringWeatherConsumer

class WeatherClusteringScheduler:
    _instance: Optional['WeatherClusteringScheduler'] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, is_worker: bool = False):
        if not self._initialized:
            logger.info("Khởi tạo WeatherClusteringScheduler")
            self.consumers = {}
            if is_worker:
                self._initialize_consumers()
            self.clustering_service = ClusteringWeatherService()
            self.database_api = DatabaseApiService()
            self._initialized = True
    
    def _initialize_consumers(self):
        """Initialize consumers based on requirements"""
        self.consumers = {
            'clustering': ClusteringWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS),
        }

    async def process_seasonal_clustering(self):
        logger.info("Bắt đầu phân tích dữ liệu phân cụm")
        try:
            if 'clustering' not in self.consumers:
                self.consumers['clustering'] = ClusteringWeatherConsumer(settings.KAFKA_BOOTSTRAP_SERVERS)
            hourly_data = self.consumers['clustering'].get_data()
            if hourly_data:
                result = await self.clustering_service.cluster_daily_data(hourly_data)
                if result is not None:
                    await self.database_api.save_clustering_analysis(result)
                logger.info("Hoàn thành phân cụm dữ liệu cho năm")
        except Exception as e:
            logger.error(f"Lỗi trong quá trình phân cụm: {str(e)}")
            raise