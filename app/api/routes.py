from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import Telemetry
from app.kafka.producer import publish_telemetry
from app.models.schemas import TelemetryAcceptedResponse, TelemetryResponse
from app.models.telemetry import RobotTelemetry

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

@router.post(
        "/telemetry",
        response_model=TelemetryAcceptedResponse)
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

    return records

