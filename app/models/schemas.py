from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TelemetryResponse(BaseModel):
    id: int
    robot_id: str
    temperature: float
    vibration: float
    motor_current: float
    timestamp: datetime
    model_config = ConfigDict(
        from_attributes=True
    )


class TelemetryAcceptedResponse(BaseModel):
    status: str
    robot_id: str
    message: str