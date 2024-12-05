from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.api.routes.prediction import router as prediction_router

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prediction_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


