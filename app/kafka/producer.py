from kafka import KafkaProducer
import json

from app.config import settings


producer = KafkaProducer(
    bootstrap_servers=settings.kafka_bootstrap_servers,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def publish_telemetry(data: dict):

    producer.send(
        settings.kafka_topic,
        value=data
    )

    producer.flush()