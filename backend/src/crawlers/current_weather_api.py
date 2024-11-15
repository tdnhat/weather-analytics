import time
import json
import logging
import requests
import pandas as pd
from typing import Dict, Any
from src.context.database import SessionLocal, DATABASE_URL
from datetime import datetime
from sqlalchemy import create_engine
from src.models.weather_data import Weather
from src.models.province import Province
from config.settings import WEATHER_API_BASE_URL, WEATHER_API_KEY


class WeatherDataIngestion:
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_API_BASE_URL
        self.connection_string = DATABASE_URL

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_raw_data(self, city: str) -> Dict[str, Any]:
        """Get raw weather data from API"""
        try:
            url = f"{self.base_url}/current.json"
            params = {
                'key': self.api_key,
                'q': city,
                'aqi': 'yes'
            }
            
            response = requests.get(url, params=params)
            self.logger.info(f"Getting data from {city}")
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error fetching data: {str(e)}")
            raise

    def to_dataframe(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert raw data to DataFrame"""
        try:
            # Flatten nested dictionary
            current_data = raw_data['current']
            weather_data = Weather(
                temp_c = current_data['temp_c'],
                feelslike_c = current_data['feelslike_c'],
                windchill_c = current_data['windchill_c'],
                heatindex_c = current_data['heatindex_c'],
                dewpoint_c = current_data['dewpoint_c'],
                wind_kph = current_data['wind_kph'],
                wind_degree = current_data['wind_degree'],
                pressure_mb = current_data['pressure_mb'],
                precip_mm = current_data['precip_mm'],
                humidity = current_data['humidity'],
                cloud = current_data['cloud'],
                uv = current_data['uv'],
                gust_kph = current_data['gust_kph'],
                last_updated_epoch = current_data['last_updated_epoch']
            )
            
            return weather_data
            
        except Exception as e:
            self.logger.error(f"Error converting to DataFrame: {str(e)}")
            raise

    def insert_to_db(self, weather_data: Weather, table_name: str = 'weather_data'):
        """Insert DataFrame into database"""
        try:
            db = SessionLocal()
            db.add(weather_data)  # Add Weather instance to session
            db.commit()  # Commit the transaction
            db.close()  # Close the session

            self.logger.info(f"Successfully inserted weather data into database")
        except Exception as e:
            self.logger.error(f"Error inserting to database: {str(e)}")
            db.rollback()  # Rollback on error
            db.close()
            raise

    def run_infinite_loop(self, interval_seconds: int = 300):
        """Run infinite loop to collect weather data"""
        db = SessionLocal()
        provinces = db.query(Province).all()

        while True:
            try:
                for province in provinces:
                    # Record start time
                    start_time = datetime.now()
                    
                    # Get and process data
                    raw_data = self.get_raw_data(province.name)  # Use province.name instead of province object
                    weather_data = self.to_dataframe(raw_data)
                    self.insert_to_db(weather_data)
                    
                    # Record end time
                    end_time = datetime.now()
                    
                    # Log the time window
                    log_entry = {
                        'start_time': start_time.isoformat(),
                        'end_time': end_time.isoformat(),
                        'city': province.name
                    }
                    
                    with open('weather_collection_log.json', 'a') as f:
                        f.write(json.dumps(log_entry) + '\n')
                    
                # Wait for next interval
                time.sleep(interval_seconds)
                
            except Exception as e:
                self.logger.error(f"Error in collection loop: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying if there's an error
