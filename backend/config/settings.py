import os
from dotenv import load_dotenv

load_dotenv()

# API Settings
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_API_BASE_URL = "http://api.weatherapi.com/v1"

# Database Settings
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'weather_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'nhat123098')
