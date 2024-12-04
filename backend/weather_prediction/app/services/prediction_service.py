import traceback
import numpy as np
import pandas as pd
from ..models.prediction import (
    HourlyWeatherData
)
from typing import List
from ..config.logging import logger

class PredictionWeatherService:
    def __init__(self):
        logger.info("Khởi tạo PredictionWeatherService")
        self.name = "prediction"

    def _get_raw_data():
        return

    async def training_model(self, hourly_data: List[HourlyWeatherData]):
        logger.info(f"Bắt đầu train dữ liệu hàng ngày với {len(hourly_data)} bản ghi")

        try:
            return

        except Exception as e:
            logger.error(f"Lỗi khi phân cụm hàng ngày: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
            raise
