from src.crawlers.weather_api import WeatherDataIngestion
from src.processors.data_processor import WeatherDataProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize crawler
        crawler = WeatherDataIngestion()
        
        # Run infinite loop for Da Nang
        crawler.run_infinite_loop(
            city="Da Nang", 
            interval_seconds=30 # 30 seconds
        )
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main()
