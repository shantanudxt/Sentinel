from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="PhysicalAI Platform",
    description="Industrial robotics data ingestion platform",
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
async def health_check():

    return {
        "status": "running",
        "service": "PhysicalAI ingestion API"
    }