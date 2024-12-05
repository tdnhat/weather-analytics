import json
import traceback
import logging
import pandas as pd
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from app.models.clustering import (
    Centroids,
    CalculateSeasonProbabilityRequest
)
from app.services.clustering_service import ClusteringWeatherService

logging.basicConfig(
    level=logging.INFO,
)

logger = logging.getLogger(__name__)  

router = APIRouter(
    prefix='/clustering'
)

@router.post('/probability')
async def calculate_season_probability(request: CalculateSeasonProbabilityRequest):
    try:
        service = ClusteringWeatherService()
        percentages_result = service._calculate_season_probability(
            centroids=request.centroids,
            temperature=request.temperature
        )
        return percentages_result
    except Exception as e:
        logger.error(f"Lỗi khi tính toán xác suất thuộc mùa của nhiệt độ: {str(e)}")
        raise
