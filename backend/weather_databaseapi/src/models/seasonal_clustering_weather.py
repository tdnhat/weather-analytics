from sqlalchemy import Column, Integer, String, Float, DateTime
from src.context.database import Base

class SeasonalClusteringWeather(Base):
    __tablename__ = "seasonal_clustering_weathers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer)
    spring_quantity = Column(Integer)
    summer_quantity = Column(Integer)
    autumn_quantity = Column(Integer)
    winter_quantity = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "year": self.year,
            "spring_quantity": self.spring_quantity,
            "summer_quantity": self.summer_quantity,
            "autumn_quantity": self.autumn_quantity,
            "winter_quantity": self.winter_quantity,
        }
