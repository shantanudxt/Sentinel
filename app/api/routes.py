from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.telemetry import RobotTelemetry
from app.database.connection import SessionLocal
from app.database.models import Telemetry


router = APIRouter(
    prefix="/api/v1",
    tags=["Telemetry"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()



@router.post("/telemetry")
async def ingest_telemetry(
    telemetry: RobotTelemetry,
    db: Session = Depends(get_db)
):

    record = Telemetry(
        robot_id=telemetry.robot_id,
        temperature=telemetry.temperature,
        vibration=telemetry.vibration,
        motor_current=telemetry.motor_current,
        timestamp=telemetry.timestamp
    )


    db.add(record)

    db.commit()

    db.refresh(record)


    return {
        "status": "stored",
        "id": record.id,
        "robot_id": record.robot_id
    }