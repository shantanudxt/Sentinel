from fastapi import APIRouter

from app.models.telemetry import RobotTelemetry


router = APIRouter(
    prefix="/api/v1",
    tags=["Telemetry"]
)


@router.post("/telemetry")
async def ingest_telemetry(
        telemetry: RobotTelemetry
):

    return {
        "status": "accepted",
        "robot_id": telemetry.robot_id,
        "message": "Telemetry received successfully"
    }