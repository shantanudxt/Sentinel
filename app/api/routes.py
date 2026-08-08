from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from kafka import KafkaProducer
from app.config import settings
from app.database.connection import SessionLocal
from app.database.models import Telemetry
from app.kafka.producer import publish_telemetry
from app.models.schemas import TelemetryAcceptedResponse, TelemetryResponse
from app.models.telemetry import RobotTelemetry

router = APIRouter(
    prefix="/api/v1",
    tags=["Telemetry"]
)

def check_kafka_connection():
    producer = KafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        bootstrap_timeout_ms=1000,
    )

    producer.close()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

@router.get("/ready")
async def readiness_check(
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))

        check_kafka_connection()

        return {
            "status": "ready"
        }

    except Exception as e:
        print(f"Readiness check failed: {e}")

        return {
            "status": "not_ready"
        }
    
@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }

@router.post(
        "/telemetry",
        response_model=TelemetryAcceptedResponse)
async def ingest_telemetry(
    telemetry: RobotTelemetry
):
    try:
        publish_telemetry(
            telemetry.model_dump(mode="json")
        )

    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="Telemetry ingestion service unavailable"
        ) 

    return {
        "status": "accepted",
        "robot_id": telemetry.robot_id,
        "message": "Telemetry queued"
    }

@router.get(
    "/telemetry",
    response_model=list[TelemetryResponse]
)
async def get_telemetry(
    db: Session = Depends(get_db)
) -> list[TelemetryResponse]:

    records = (
        db.query(Telemetry)
        .order_by(
            Telemetry.timestamp.desc()
        )
        .limit(100)
        .all()
    )

    return records

@router.get(
    "/robots/{robot_id}/telemetry",
    response_model=list[TelemetryResponse]
)
async def get_robot_telemetry(
    robot_id: str,
    db: Session = Depends(get_db)
) -> list[TelemetryResponse]:

    records = (
        db.query(Telemetry)
        .filter(
            Telemetry.robot_id == robot_id
        )
        .order_by(
            Telemetry.timestamp.desc()
        )
        .limit(100)
        .all()
    )

    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No telemetry found for robot {robot_id}"
        )

    return records

