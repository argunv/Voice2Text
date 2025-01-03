from fastapi import FastAPI

from app.api.rest.endpoints import transcription, minio, health

app = FastAPI()

# Include routes
app.include_router(transcription.router, prefix="/api", tags=["transcriptions"])
app.include_router(minio.router, prefix="/minio", tags=["minio"])
app.include_router(health.router, tags=["health"])
