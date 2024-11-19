import asyncio
from src.crawlers.weather_historical_crawler import HistoricalWeatherCrawler
import json
import os
from datetime import datetime, timedelta
import time

async def run_crawler():
    historical_weather_crawler = HistoricalWeatherCrawler()
    default_start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        log_file_path = '/app/weather_data_ingestion/weather_log.json'

        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                logs = json.load(f)
                if logs:
                    last_end_date = logs[-1]['end_date']
                    start_date = (datetime.strptime(last_end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    start_date = default_start_date
        else:
            start_date = default_start_date
        
        print(f"Starting crawl from: {start_date}")
        await historical_weather_crawler.craw_historical_weather(start_date=start_date, interval_seconds=15)
    except Exception as e:
        print(f"Error reading log file: {str(e)}")
        print(f"Starting with default date: {default_start_date}")
        return

if __name__ == "__main__":
    TWO_HOURS = 2 * 60 * 60  # 2 hours in seconds
    
    while True:
        print(f"Starting crawler at {datetime.now()}")
        asyncio.run(run_crawler())
        print(f"Crawler finished at {datetime.now()}. Sleeping for 2 hours...")
        time.sleep(TWO_HOURS)