import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_BASE_URL = os.getenv('WEATHER_API_BASE_URL')
DATABASEAPI_URL = os.getenv('DATABASEAPI_URL')
