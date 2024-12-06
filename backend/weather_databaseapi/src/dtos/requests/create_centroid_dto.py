from pydantic import BaseModel
from datetime import datetime

class CreateCentroidDto(BaseModel):
    model_config = {
        'from_attributes': True,
    }

    spring_centroid: float
    summer_centroid: float
    autumn_centroid: float
    winter_centroid: float