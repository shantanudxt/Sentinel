from datetime import datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.main import app
from app.api.routes import get_db
from app.database.connection import Base
from app.database.models import Telemetry


client = TestClient(app)

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

@patch(
    "app.api.routes.publish_telemetry"
)
def test_ingest_telemetry(mock_publish):

    payload = {
        "robot_id": "ARM-001",
        "temperature": 72.5,
        "vibration": 0.04,
        "motor_current": 3.2,
        "timestamp": "2026-08-07T17:00:00Z"
    }


    response = client.post(
        "/api/v1/telemetry",
        json=payload
    )


    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "accepted"

    assert data["robot_id"] == "ARM-001"

    mock_publish.assert_called_once()

def test_ingest_telemetry_rejects_invalid_temperature():

    payload = {
        "robot_id": "ARM-001",
        "temperature": -999,
        "vibration": 0.04,
        "motor_current": 3.2,
        "timestamp": "2026-08-07T17:00:00Z"
    }

    response = client.post(
        "/api/v1/telemetry",
        json=payload
    )

    assert response.status_code == 422

def test_get_telemetry(db_session):

    telemetry = Telemetry(
        robot_id="ARM-001",
        temperature=72.5,
        vibration=0.04,
        motor_current=3.2,
        timestamp=datetime.now()
    )

    db_session.add(telemetry)
    db_session.commit()
    db_session.refresh(telemetry)

    response = client.get(
        "/api/v1/telemetry"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["robot_id"] == "ARM-001"
    assert data[0]["temperature"] == 72.5
    assert data[0]["vibration"] == 0.04
    assert data[0]["motor_current"] == 3.2
