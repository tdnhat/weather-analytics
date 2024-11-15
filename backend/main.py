import threading
from fastapi import FastAPI
from src.api.routes import province
from contextlib import asynccontextmanager
from src.context.database import Base, engine
from src.crawlers.current_weather_api import WeatherDataIngestion

@asynccontextmanager
async def lifespan(app: FastAPI):
    global weather_thread_running
    weather_thread_running = True

    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    def run_weather_digesting():
        global weather_thread_running  # Add this line
        current_weather_crawler = WeatherDataIngestion()
        while weather_thread_running:
            try:
                current_weather_crawler.run_infinite_loop(interval_seconds=300)
            except Exception as e:
                print(f"Error in weather thread: {str(e)}")
                weather_thread_running = False
                break

    thread = threading.Thread(target=run_weather_digesting, daemon=True)
    thread.start()

    yield

app = FastAPI(
    title = "Weather Analytics API",
    description = "API for weather analytics",
    version = "1.0.0",
    lifespan = lifespan
)

# Include the router
app.include_router(province.router)
