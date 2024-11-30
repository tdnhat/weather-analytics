import asyncio
import aiohttp
import aiofiles
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
        self.log_file = '/app/weather_log.json'
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def write_log(self, log_entry: dict):
        try:
            # Read existing logs
            existing_logs = []
            if os.path.exists(self.log_file):
                async with aiofiles.open(self.log_file, 'r') as f:
                    content = await f.read()
                    try:
                        existing_logs = json.loads(content)
                    except json.JSONDecodeError:
                        existing_logs = []
            
            # Append new log
            existing_logs.append(log_entry)
            
            # Write back with pretty formatting
            async with aiofiles.open(self.log_file, 'w') as f:
                await f.write(json.dumps(existing_logs, indent=4))
                
            self.logger.info(f"Successfully wrote log entry for {log_entry.get('end_date')}")
        except Exception as e:
            self.logger.error(f"Failed to write log: {str(e)}")
    
    async def get_raw_data(self, city: str = 'Thua Thien Hue', date: str = None) -> Dict[str, Any]:
        try:
            url = f"{self.base_url}/history.json"
            params = {
                'q': city,
                'dt': date,
                'aqi': 'yes',
                'key': self.api_key
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    self.logger.info(f"Getting raw data from {city} on {date}")
                    response.raise_for_status()
                    return await response.json()
                    
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
                    time=datetime.strptime(hour['time'], '%Y-%m-%d %H:%M').isoformat(),
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

    async def craw_historical_weather(self, start_date: str, interval_seconds: int = 300):
        try:
            current_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.now()
            
            self.logger.info(f"Starting data collection from {start_date} to {end_date.strftime('%Y-%m-%d')}")
            
            async with aiohttp.ClientSession() as session:
                while current_date.date() < end_date.date():
                    try:
                        date_str = current_date.strftime('%Y-%m-%d')
                        self.logger.info(f"Processing date: {date_str}")
                        
                        # Get and process data
                        raw_data = await self.get_raw_data(date=date_str)
                        weather_data_list = self.flatten_raw_data(raw_data)
                        weather_dict_list = [weather.__dict__ for weather in weather_data_list]

                        # Insert data to database
                        url = f"{DATABASEAPI_URL}/weather-raw/insert"
                        async with session.post(url, json=weather_dict_list) as response:
                            if response.status == 200:
                                self.logger.info("Weather data created successfully!")
                            else:
                                self.logger.error(f"Error: {await response.text()}")
                        
                        # Log the entry
                        log_entry = {
                            'end_date': date_str,
                            'records_count': len(weather_data_list),
                            'timestamp': datetime.now().isoformat()
                        }
                        await self.write_log(log_entry)
                        
                        # Move to next day
                        current_date += timedelta(days=1)
                        
                        # Wait before next API call
                        await asyncio.sleep(interval_seconds)
                        
                    except Exception as e:
                        self.logger.error(f"Error processing date {date_str}: {str(e)}")
                        await asyncio.sleep(60)
            
            self.logger.info("Data collection completed - reached current date")
            
        except Exception as e:
            self.logger.error(f"Fatal error in collection loop: {str(e)}")
            raise
