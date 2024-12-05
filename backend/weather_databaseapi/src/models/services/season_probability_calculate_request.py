from ast import Dict
from re import I
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Centroids(BaseModel):
    spring_centroid: float
    summer_centroid: float
    autumn_centroid: float
    winter_centroid: float

class CalculateSeasonProbabilityRequest(BaseModel):
    centroids: Centroids
    temperature: float

    def to_dict(self):
        # Convert the object's attributes to a dictionary
        return {
            "centroids": self.centroids.dict(),
            "temperature": self.temperature
        }