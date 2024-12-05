import os
from dotenv import load_dotenv

load_dotenv()

# Database Settings
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

PREDICTION_API_BASE_URL = os.getenv('PREDICTION_API_BASE_URL')
CLUSTERING_API_BASE_URL = os.getenv('CLUSTERING_API_BASE_URL')
