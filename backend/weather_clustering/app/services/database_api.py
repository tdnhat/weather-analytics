import httpx
import traceback
from datetime import datetime
from ..config.logging import logger
from ..config.settings import settings
from ..models.clustering import (
    ClusteringResultData
)

class DatabaseApiService:
    def __init__(self):
        logger.info("Khởi tạo DatabaseApiService của service weather_clustering")
        self.base_url = settings.DATABASE_API_URL
        
    async def save_clustering_analysis(self, cluster_data: ClusteringResultData):
        logger.info(f"Đang lưu dữ liệu phân cụm và centroid")
        try:
            async with httpx.AsyncClient() as client:
                seasonal_quantity_list = cluster_data.quantity
                for seasonal_quantity in seasonal_quantity_list:
                    response = await client.post(
                        f"{self.base_url}/api/clustering/seasonal",
                        json=seasonal_quantity.model_dump()
                    )
                    response.raise_for_status()
                    logger.info(f"Lưu dữ liệu phân cụm số lượng mùa cho năm {seasonal_quantity.year} thành công")

                result_response = await client.post(
                    f"{self.base_url}/api/clustering/centroids",
                    json=cluster_data.centroids.model_dump()
                )
                result_response.raise_for_status()
                logger.info(f"Lưu dữ liệu phân cụm centroids thành công") 

        except Exception as e:
            logger.error(f"Lỗi khi lưu clustering analysis: {str(e)}")
            logger.error(f"Chi tiết lỗi: {traceback.format_exc()}")
            raise