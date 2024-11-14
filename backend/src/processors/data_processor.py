from sqlalchemy import create_engine
import pandas as pd
from config.settings import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

class WeatherDataProcessor:
    def __init__(self):
        self.engine = create_engine(
            f'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        )
    
    def save_to_db(self, df: pd.DataFrame, table_name: str = 'weather_data'):
        """Save DataFrame to MySQL database"""
        try:
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists='append',
                index=False
            )
        except Exception as e:
            raise Exception(f"Error saving to database: {str(e)}")
