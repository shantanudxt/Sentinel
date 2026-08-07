from datetime import datetime
from pydantic import BaseModel, Field


class RobotTelemetry(BaseModel):
    """
    Represents telemetry data received from industrial robots.
    """

    robot_id: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique robot identifier",
        example="ARM-001"
    )

    temperature: float = Field(
        ...,
        ge=-50, #can't validate precisely before knowing more about the sensors/domain
        le=200,
        description="Motor temperature in Celsius",
        example=72.5
    )

    vibration: float = Field(
        ...,
        ge=0,
        le=100,
        description="Robot vibration level",
        example=0.04
    )

    motor_current: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Motor electrical current",
        example=3.2
    )

    timestamp: datetime = Field(
        ...,
        description="Telemetry event timestamp"
    )