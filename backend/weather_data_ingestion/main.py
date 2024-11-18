from src.crawlers.weather_historical_crawler import HistoricalWeatherCrawler
import json
import os
from datetime import datetime, timedelta
import time

def run_crawler():
    historical_weather_crawler = HistoricalWeatherCrawler()
    default_start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    try:
        if os.path.exists('weather_log.json'):
            with open('weather_log.json', 'r') as f:
                logs = json.load(f)
                if logs:
                    last_end_date = logs[-1]['end_date']
                    start_date = (datetime.strptime(last_end_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                else:
                    start_date = default_start_date
        else:
            start_date = default_start_date
        
        print(f"Starting crawl from: {start_date}")
        historical_weather_crawler.craw_historical_weather(start_date=start_date, interval_seconds=15)
    except Exception as e:
        print(f"Error reading log file: {str(e)}")
        print(f"Starting with default date: {default_start_date}")
        historical_weather_crawler.craw_historical_weather(start_date=default_start_date, interval_seconds=15)

if __name__ == "__main__":
    TWO_HOURS = 2 * 60 * 60  # 2 hours in seconds
    
    while True:
        print(f"Starting crawler at {datetime.now()}")
        run_crawler()
        print(f"Crawler finished at {datetime.now()}. Sleeping for 2 hours...")
        time.sleep(TWO_HOURS)