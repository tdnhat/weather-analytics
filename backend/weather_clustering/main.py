from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.clustering import router as clustering_router

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clustering_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}




