import json
from datetime import datetime

from kafka import KafkaConsumer
from kafka.serializer import Deserializer
from sqlalchemy.orm import Session

from app.config import settings
from app.database.connection import SessionLocal
from app.database.models import Telemetry

class JsonDeserializer(Deserializer):
    def deserialize(self, *args):
        data = args[-1]
        return json.loads(data.decode("utf-8"))

consumer = KafkaConsumer(
    settings.kafka_topic,

    bootstrap_servers=settings.kafka_bootstrap_servers,

    value_deserializer=JsonDeserializer(),

    auto_offset_reset="earliest",

    enable_auto_commit=False,

    group_id="telemetry-processing-group"
)


def process_telemetry(data: dict, db: Session):
    telemetry = Telemetry(
        robot_id=data["robot_id"],
        temperature=data["temperature"],
        vibration=data["vibration"],
        motor_current=data["motor_current"],
        timestamp=datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        )
    )

    db.add(telemetry)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise


def start_consumer():

    print("Kafka consumer started...")

    db = SessionLocal()

    try:

        for message in consumer:

            telemetry_data = message.value

            print(
                "Received:",
                telemetry_data
            )

            process_telemetry(
                telemetry_data,
                db
            )

            consumer.commit()

    finally:

        db.close()


if __name__ == "__main__":

    start_consumer()