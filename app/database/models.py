from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.connection import Base


class Telemetry(Base):

    __tablename__ = "robot_telemetry"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    robot_id = Column(
        String,
        index=True
    )


    temperature = Column(
        Float
    )


    vibration = Column(
        Float
    )


    motor_current = Column(
        Float
    )


    timestamp = Column(
        DateTime
    )