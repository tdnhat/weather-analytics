from typing import Dict, Any
import requests
import logging
import pandas as pd
from datetime import datetime
from os import getenv
import time
import json

class WeatherDataIngestion:
    def __init__(self):
        self.api_key = getenv('WEATHER_API_KEY')
        self.base_url = getenv('WEATHER_API_BASE_URL')
        
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
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error fetching data: {str(e)}")
            raise

    def to_dataframe(self, raw_data: Dict[str, Any]) -> pd.DataFrame:
        """Convert raw data to DataFrame"""
        try:
            # Flatten nested dictionary
            flat_data = {
                'city': raw_data['location']['name'],
                'country': raw_data['location']['country'],
                'lat': raw_data['location']['lat'],
                'lon': raw_data['location']['lon'],
                'temp_c': raw_data['current']['temp_c'],
                'humidity': raw_data['current']['humidity'],
                'condition': raw_data['current']['condition']['text'],
                'wind_kph': raw_data['current']['wind_kph'],
                'timestamp': datetime.now().isoformat()
            }
            
            return pd.DataFrame([flat_data])
            
        except Exception as e:
            self.logger.error(f"Error converting to DataFrame: {str(e)}")
            raise

    def insert_to_db(self, df: pd.DataFrame, table_name: str = 'weather_data'):
        """Insert DataFrame into database"""
        try:
            from sqlalchemy import create_engine
            engine = create_engine(getenv('DATABASE_URL'))
            
            # Insert data into database
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists='append',
                index=False
            )
            self.logger.info(f"Successfully inserted {len(df)} rows into {table_name}")
            
        except Exception as e:
            self.logger.error(f"Error inserting to database: {str(e)}")
            raise

    def run_infinite_loop(self, city: str, interval_seconds: int = 300):
        """Run infinite loop to collect weather data"""
        while True:
            try:
                # Record start time
                start_time = datetime.now()
                
                # Get and process data
                raw_data = self.get_raw_data(city)
                df = self.to_dataframe(raw_data)
                self.insert_to_db(df)
                
                # Record end time
                end_time = datetime.now()
                
                # Log the time window
                log_entry = {
                    'start_time': start_time.isoformat(),
                    'end_time': end_time.isoformat(),
                    'city': city
                }
                
                with open('weather_collection_log.json', 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
                
                # Wait for next interval
                time.sleep(interval_seconds)
                
            except Exception as e:
                self.logger.error(f"Error in collection loop: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying if there's an error
