from ast import Dict
from re import I
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HourlyWeatherData(BaseModel):
    Id: int
    TimeEpoch: int
    Time: str
    TempC: float
    Humidity: int
    PrecipMm: float
    WindKph: float
    PressureMb: float
    FeelslikeC: float
    WindchillC: float
    HeatindexC: float
    DewpointC: float
    WindDegree: int
    WindDir: str
    

class ClusteringWeatherData(BaseModel):
    year: int
    spring_quantity: int
    summer_quantity: int
    autumn_quantity: int
    winter_quantity: int
    spring_centroid: float
    summer_centroid: float
    autumn_centroid: float
    winter_centroid: float

class Centroids(BaseModel):
    spring_centroid: float
    summer_centroid: float
    autumn_centroid: float
    winter_centroid: float

class SeasonQuantityData(BaseModel):
    year: int
    spring_quantity: int
    summer_quantity: int
    autumn_quantity: int
    winter_quantity: int

class ClusteringResultData(BaseModel):
    centroids: Centroids
    quantity: List[SeasonQuantityData]
