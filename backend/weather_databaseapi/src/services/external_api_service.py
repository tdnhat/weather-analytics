import requests
import logging
from config import settings
from src.models.services.weather_prediction_request import (
    PredictionWeatherRequest
)
from src.models.services.season_probability_calculate_request import (
    CalculateSeasonProbabilityRequest
)

class ExternalApiService():
    def __init__(self):
        self.prediction_base_url = settings.PREDICTION_API_BASE_URL
        self.clustering_base_url = settings.CLUSTERING_API_BASE_URL

    def get_weather_prediction(self, prediction_request: PredictionWeatherRequest):
        response = requests.post(
            f"{self.prediction_base_url}/api/prediction/weather",
            json=prediction_request.to_dict()
        )

        return response
    
    def get_season_probability(self, calculation_request: CalculateSeasonProbabilityRequest):
        response = requests.post(
            f"{self.clustering_base_url}/api/clustering/probability",
            json=calculation_request.to_dict()
        )

        return response
    