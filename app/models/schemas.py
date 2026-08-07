from datetime import datetime
from pydantic import BaseModel


class TelemetryResponse(BaseModel):
    id: int
    robot_id: str
    temperature: float
    vibration: float
    motor_current: float
    timestamp: datetime
    class Config:
        from_attributes = True


class TelemetryAcceptedResponse(BaseModel):
    status: str
    robot_id: str
    message: str