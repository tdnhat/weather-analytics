from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.context.database import Base, engine
from src.api.routes.analysis import router as analysis_router
from src.api.routes.clustering import router as clustering_router
from src.api.routes.weather_raw_routes import router as weather_raw_router

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather_raw_router)
app.include_router(analysis_router)
app.include_router(clustering_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


