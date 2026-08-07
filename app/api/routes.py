from fastapi import APIRouter

from app.models.telemetry import RobotTelemetry
from app.kafka.producer import publish_telemetry


router = APIRouter(
    prefix="/api/v1",
    tags=["Telemetry"]
)


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