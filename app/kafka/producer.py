from kafka import KafkaProducer
import json
import os

from app.config import settings


def get_producer():

    return KafkaProducer(
        bootstrap_servers=os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS",
            "localhost:9092"
        ),
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )


def publish_telemetry(data: dict):

    producer = get_producer()
    
    producer.send(
        settings.kafka_topic,
        value=data
    )

    producer.flush()