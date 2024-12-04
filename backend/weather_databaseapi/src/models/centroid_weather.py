from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class SeasonalWeatherCentroid(Base):
    __tablename__ = "seasonal_clustering_centroids"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    spring_centroid = Column(Float)
    summer_centroid = Column(Float)
    autumn_centroid = Column(Float)
    winter_centroid = Column(Float)

    def to_dict(self):
        return {
            "id": self.id,
            "spring_centroid": self.spring_centroid,
            "summer_centroid": self.summer_centroid,
            "autumn_centroid": self.autumn_centroid,
            "winter_centroid": self.winter_centroid
        }
