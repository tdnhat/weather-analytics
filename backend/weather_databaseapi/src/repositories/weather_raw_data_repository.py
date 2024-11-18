from src.models.weather_data import Weather
from src.context.database import SessionLocal

def insert_weather_raw_data(self, weather_data_list: list[Weather], table_name: str = 'weather_raw_data'):
    """Insert DataFrame into database"""
    try:
        db = SessionLocal()
        db.add_all(weather_data_list)  # Add Weather instance to session
        db.commit()  # Commit the transaction
        db.close()  # Close the session

        self.logger.info(f"Successfully inserted {len(weather_data_list)}")
    except Exception as e:
        self.logger.error(f"Error inserting to database: {str(e)}")
        db.rollback()  # Rollback on error
        db.close()
        raise