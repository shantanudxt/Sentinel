from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.telemetry import RobotTelemetry
from app.kafka.producer import publish_telemetry

from app.database.connection import SessionLocal
from app.database.models import Telemetry

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

router = APIRouter(
    prefix="/api/v1",
    tags=["Telemetry"]
)

@router.get("/telemetry")
async def get_telemetry(
    db: Session = Depends(get_db)
):

    records = (
        db.query(Telemetry)
        .order_by(
            Telemetry.timestamp.desc()
        )
        .limit(100)
        .all()
    )

    return records

@router.get("/robots/{robot_id}/telemetry")
async def get_robot_telemetry(
    robot_id: str,
    db: Session = Depends(get_db)
):

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

    return records

@router.post("/telemetry")
async def ingest_telemetry(
    telemetry: RobotTelemetry
):

    publish_telemetry(
        telemetry.model_dump(mode="json")
    )

    return {
        "status": "accepted",
        "robot_id": telemetry.robot_id,
        "message": "Telemetry queued"
    }