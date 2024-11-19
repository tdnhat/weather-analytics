from fastapi import FastAPI
from src.context.database import Base, engine
from src.api.routes.weather_raw_routes import router as weather_raw_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

app.include_router(weather_raw_router)
