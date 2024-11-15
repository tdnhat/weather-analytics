import requests
from src.models.province import Province
from src.data.vietnam_provinces import province_names
from config.settings import WEATHER_API_BASE_URL, WEATHER_API_KEY
from main import SessionLocal

def seed_provinces():
    db = SessionLocal()
    try:
        for province_name in province_names:
            url = f"{WEATHER_API_BASE_URL}/current.json"
            params = {
                'key': WEATHER_API_KEY,
                'q': province_name,
                'aqi': 'yes'
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            province = Province(
                name=data['location']['name'],
                region=data['location']['region'],
                country=data['location']['country'],
                lat=data['location']['lat'],
                lon=data['location']['lon'],
            )
            db.add(province)
        
        db.commit()
    except Exception as e:
        print(f"Error seeding provinces: {str(e)}")
        db.rollback()
    finally:
        db.close()
