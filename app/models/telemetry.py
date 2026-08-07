from datetime import datetime
from pydantic import BaseModel, Field


class RobotTelemetry(BaseModel):
    """
    Represents telemetry data received from industrial robots.
    """

    robot_id: str = Field(
        ...,
        description="Unique robot identifier",
        example="ARM-001"
    )

    temperature: float = Field(
        ...,
        description="Motor temperature in Celsius",
        example=72.5
    )

    vibration: float = Field(
        ...,
        description="Robot vibration level",
        example=0.04
    )

    motor_current: float = Field(
        ...,
        description="Motor electrical current",
        example=3.2
    )

    timestamp: datetime