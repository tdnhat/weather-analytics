from pydantic import BaseModel
from datetime import datetime

class CreateSeasonalClustering(BaseModel):
    model_config = {
        'from_attributes': True,
        'json_encoders': {
            datetime: lambda v: v.isoformat()  # Convert datetime to ISO format string
        }
    }

    year: int
    spring_quantity: int
    summer_quantity: int
    autumn_quantity: int
    winter_quantity: int