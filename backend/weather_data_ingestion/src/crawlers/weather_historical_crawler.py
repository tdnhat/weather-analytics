import os
import time
import json
import logging
import requests
import pandas as pd
from typing import Dict, Any
from datetime import datetime, timedelta
from src.models.weather_data import Weather
from config.settings import WEATHER_API_BASE_URL, WEATHER_API_KEY, DATABASEAPI_URL

class HistoricalWeatherCrawler:
    def __init__(self):
        self.api_key = WEATHER_API_KEY
        self.base_url = WEATHER_API_BASE_URL
        self.log_file = 'weather_log.json'
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def write_log(self, log_entry: dict):
        try:
            # Read existing logs
            existing_logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    try:
                        existing_logs = json.load(f)
                    except json.JSONDecodeError:
                        existing_logs = []
            
            # Append new log
            existing_logs.append(log_entry)
            
            # Write back with pretty formatting
            with open(self.log_file, 'w') as f:
                json.dump(existing_logs, f, indent=4)
                
            self.logger.info(f"Successfully wrote log entry for {log_entry.get('end_date')}")
        except Exception as e:
            self.logger.error(f"Failed to write log: {str(e)}")
    
    def get_raw_data(self, city: str = 'Thua Thien Hue', date: str = None) -> Dict[str, Any]:
        """
            Get raw weather data from API
            
            Args:
            city (str): Tên thành phố muốn lấy dữ liệu
            date (str): Ngày muốn lấy dữ liệu dưới dạng YYYY-MM-DD
        """
        try:
            url = f"{self.base_url}/history.json"
            params = {
                'q': city,
                'dt': date,
                'aqi': 'yes',
                'key': self.api_key
            }
            
            response = requests.get(url, params=params)
            self.logger.info(f"Getting raw data from {city} on {date}")
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error fetching data: {str(e)}")
            raise

    def flatten_raw_data(self, raw_data: Dict[str, Any]) -> list[Weather]:
        """Convert raw data to Weather instance"""
        try:
            weather_data_list = []
            # Flatten nested dictionary
            hours_list = raw_data['forecast']['forecastday'][0]['hour']
            for hour in hours_list:
                weather_data = Weather(
                    time_epoch=hour['time_epoch'],
                    time=datetime.strptime(hour['time'], '%Y-%m-%d %H:%M'),
                    temp_c=hour['temp_c'],
                    temp_f=hour['temp_f'],
                    is_day=hour['is_day'],
                    condition_text=hour['condition']['text'],
                    condition_icon=hour['condition']['icon'],
                    condition_code=hour['condition']['code'],
                    wind_mph=hour['wind_mph'],
                    wind_kph=hour['wind_kph'],
                    wind_degree=hour['wind_degree'],
                    wind_dir=hour['wind_dir'],
                    pressure_mb=hour['pressure_mb'],
                    pressure_in=hour['pressure_in'],
                    precip_mm=hour['precip_mm'],
                    precip_in=hour['precip_in'],
                    snow_cm=hour['snow_cm'],
                    humidity=hour['humidity'],
                    cloud=hour['cloud'],
                    feelslike_c=hour['feelslike_c'],
                    feelslike_f=hour['feelslike_f'],
                    windchill_c=hour['windchill_c'],
                    windchill_f=hour['windchill_f'],
                    heatindex_c=hour['heatindex_c'],
                    heatindex_f=hour['heatindex_f'],
                    dewpoint_c=hour['dewpoint_c'],
                    dewpoint_f=hour['dewpoint_f'],
                    will_it_rain=hour['will_it_rain'],
                    chance_of_rain=hour['chance_of_rain'],
                    will_it_snow=hour['will_it_snow'],
                    chance_of_snow=hour['chance_of_snow'],
                    vis_km=hour['vis_km'],
                    vis_miles=hour['vis_miles'],
                    gust_mph=hour['gust_mph'],
                    gust_kph=hour['gust_kph'],
                    uv=hour['uv']
                )
                weather_data_list.append(weather_data)

            return weather_data_list
            
        except Exception as e:
            self.logger.error(f"Error converting to DataFrame: {str(e)}")
            raise

    def craw_historical_weather(self, start_date: str, interval_seconds: int = 300):
        """
            Run loop to collect weather data from start_date until current date
            
            Args:
                start_date (str): Start date in YYYY-MM-DD format
                interval_seconds (int): Seconds to wait between API calls
        """
        try:
            current_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.now()
            
            self.logger.info(f"Starting data collection from {start_date} to {end_date.strftime('%Y-%m-%d')}")
            
            while current_date.date() <= end_date.date():
                try:
                    # Format current date for API call
                    date_str = current_date.strftime('%Y-%m-%d')
                    self.logger.info(f"Processing date: {date_str}")
                    
                    # Get and process data
                    raw_data = self.get_raw_data(date=date_str)
                    weather_data_list = self.flatten_raw_data(raw_data)

                    # Convert Weather objects to dictionaries
                    weather_dict_list = [
                        {
                            "time_epoch": weather.time_epoch,
                            "time": weather.time.isoformat(),
                            "temp_c": weather.temp_c,
                            "temp_f": weather.temp_f,
                            "is_day": weather.is_day,
                            "condition_text": weather.condition_text,
                            "condition_icon": weather.condition_icon,
                            "condition_code": weather.condition_code,
                            "wind_mph": weather.wind_mph,
                            "wind_kph": weather.wind_kph,
                            "wind_degree": weather.wind_degree,
                            "wind_dir": weather.wind_dir,
                            "pressure_mb": weather.pressure_mb,
                            "pressure_in": weather.pressure_in,
                            "precip_mm": weather.precip_mm,
                            "precip_in": weather.precip_in,
                            "snow_cm": weather.snow_cm,
                            "humidity": weather.humidity,
                            "cloud": weather.cloud,
                            "feelslike_c": weather.feelslike_c,
                            "feelslike_f": weather.feelslike_f,
                            "windchill_c": weather.windchill_c,
                            "windchill_f": weather.windchill_f,
                            "heatindex_c": weather.heatindex_c,
                            "heatindex_f": weather.heatindex_f,
                            "dewpoint_c": weather.dewpoint_c,
                            "dewpoint_f": weather.dewpoint_f,
                            "will_it_rain": weather.will_it_rain,
                            "chance_of_rain": weather.chance_of_rain,
                            "will_it_snow": weather.will_it_snow,
                            "chance_of_snow": weather.chance_of_snow,
                            "vis_km": weather.vis_km,
                            "vis_miles": weather.vis_miles,
                            "gust_mph": weather.gust_mph,
                            "gust_kph": weather.gust_kph,
                            "uv": weather.uv
                        }
                        for weather in weather_data_list
                    ]

                    # Insert data to database
                    url = f"{DATABASEAPI_URL}/weather-raw/insert"
                    response = requests.post(
                        url,
                        json=weather_dict_list
                    )
                    
                    # Log the endate entry when finish crawling
                    log_entry = {
                        'end_date': date_str,
                        'records_count': len(weather_data_list),
                        'timestamp': datetime.now().isoformat()
                    }

                    # Check response
                    if response.status_code == 200:
                        self.logger.info("Weather data created successfully!")
                    else:
                        self.logger.info(f"Error: {response.content}")
                    
                    self.write_log(log_entry)
                    
                    # Move to next day
                    current_date += timedelta(days=1)
                    
                    # Wait before next API call to respect rate limits
                    time.sleep(interval_seconds)
                    
                except Exception as e:
                    self.logger.error(f"Error processing date {date_str}: {str(e)}")
                    time.sleep(60)  # Wait a minute before retrying if there's an error
            
            self.logger.info("Data collection completed - reached current date")
            
        except Exception as e:
            self.logger.error(f"Fatal error in collection loop: {str(e)}")
            raise
