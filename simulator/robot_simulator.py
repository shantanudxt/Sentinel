import random
import time
from datetime import datetime, timezone

import requests


INGESTION_URL = "http://localhost:8000/api/v1/telemetry"


def generate_telemetry():

    return {
        "robot_id": "ARM-001",
        "temperature": round(
            random.uniform(60, 90),
            2
        ),
        "vibration": round(
            random.uniform(0.01, 0.10),
            3
        ),
        "motor_current": round(
            random.uniform(2.0, 5.0),
            2
        ),
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat()
    }


def send_telemetry(data):

    response = requests.post(
        INGESTION_URL,
        json=data
    )

    response.raise_for_status()

    print(response.json())


if __name__ == "__main__":

    while True:

        telemetry = generate_telemetry()

        print(
            "Sending:",
            telemetry
        )

        send_telemetry(telemetry)

        time.sleep(5)