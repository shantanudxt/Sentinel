from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="PhysicalAI Platform",
    description="Industrial robotics data ingestion platform",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)


@app.get("/")
async def health_check():
    return {
        "status": "running",
        "service": "PhysicalAI ingestion API"
    }
