from typing import List
import httpx
from ..models.analysis import DailyAnalysis, CorrelationAnalysis, SeasonalAnalysis
from ..config.settings import settings
from ..config.logging import logger

class DatabaseApiService:
    def __init__(self):
        logger.info("Khởi tạo DatabaseApiService")
        self.base_url = settings.DATABASE_API_URL
        
    async def save_daily_analysis(self, analysis: DailyAnalysis):
        logger.info(f"Đang lưu phân tích hàng ngày cho ngày {analysis.date}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/analysis/daily",
                    json=analysis.model_dump()
                )
                response.raise_for_status()
            logger.info("Lưu phân tích hàng ngày thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu daily analysis: {str(e)}")
            raise

    async def save_correlation_analysis(self, analysis: CorrelationAnalysis):
        logger.info(f"Đang lưu phân tích tương quan cho ngày {analysis.date}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/analysis/correlation",
                    json=analysis.model_dump()
                )
                response.raise_for_status()
            logger.info("Lưu phân tích tương quan thành công")
        except Exception as e:
            logger.error(f"Lỗi khi lưu correlation analysis: {str(e)}")
            raise

    async def save_seasonal_analysis(self, analyses: List[SeasonalAnalysis]):
        logger.info(f"Đang lưu {len(analyses)} phân tích theo quý")
        try:
            async with httpx.AsyncClient() as client:
                for analysis in analyses:
                    logger.info(f"Đang lưu phân tích theo mùa cho ngày {analysis.date}")
                    response = await client.post(
                        f"{self.base_url}/api/analysis/seasonal",
                        json=analysis.model_dump()
                    )
                    response.raise_for_status()
                    logger.info(f"Lưu phân tích theo quý cho ngày {analysis.date} thành công")
            logger.info("Hoàn thành lưu tất cả phân tích theo mùa")
        except Exception as e:
            logger.error(f"Lỗi khi lưu seasonal analysis: {str(e)}")
            raise