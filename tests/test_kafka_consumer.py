from unittest.mock import MagicMock, patch

import pytest

from app.kafka.consumer import process_telemetry, start_consumer

def test_consumer_commits_offset_after_successful_persistence():
    db = MagicMock()

    message = MagicMock()
    message.value = {
        "robot_id": "ARM-001",
        "temperature": 72.5,
        "vibration": 0.04,
        "motor_current": 3.2,
        "timestamp": "2026-08-07T17:00:00Z"
    }

    mock_consumer = MagicMock()
    mock_consumer.__iter__.return_value = [message]

    with patch(
        "app.kafka.consumer.get_consumer",
        return_value=mock_consumer
    ), patch(
        "app.kafka.consumer.SessionLocal",
        return_value=db
    ):
        start_consumer()

    mock_consumer.commit.assert_called_once()

def test_consumer_does_not_commit_offset_when_persistence_fails():
    db = MagicMock()
    db.commit.side_effect = Exception("Database error")

    message = MagicMock()
    message.value = {
        "robot_id": "ARM-001",
        "temperature": 72.5,
        "vibration": 0.04,
        "motor_current": 3.2,
        "timestamp": "2026-08-07T17:00:00Z"
    }

    mock_consumer = MagicMock()
    mock_consumer.__iter__.return_value = [message]

    with patch(
        "app.kafka.consumer.get_consumer",
        return_value=mock_consumer
    ), patch(
        "app.kafka.consumer.SessionLocal",
        return_value=db
    ):
        with pytest.raises(Exception, match="Database error"):
            start_consumer()

    mock_consumer.commit.assert_not_called()

def test_process_telemetry_commits_transaction():
    db = MagicMock()

    data = {
        "robot_id": "ARM-001",
        "temperature": 72.5,
        "vibration": 0.04,
        "motor_current": 3.2,
        "timestamp": "2026-08-07T17:00:00Z"
    }

    process_telemetry(data, db)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.rollback.assert_not_called()


def test_process_telemetry_rolls_back_on_database_error():
    db = MagicMock()

    db.commit.side_effect = Exception("Database error")

    data = {
        "robot_id": "ARM-001",
        "temperature": 72.5,
        "vibration": 0.04,
        "motor_current": 3.2,
        "timestamp": "2026-08-07T17:00:00Z"
    }

    with pytest.raises(Exception, match="Database error"):
        process_telemetry(data, db)

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.rollback.assert_called_once()