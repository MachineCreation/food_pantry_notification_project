#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:test_log_record
# Author: Justin Crump
# 2026-05-26
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Unit tests for LogRecord.
# These tests verify that:
# - Values passed into the constructor are stored correctly
# - None values are preserved without modification
# - Getter methods return exactly what was provided

# Local Imports
from app.logic.models.LogRecord import LogRecord

# Python Imports
from datetime import datetime

def test_log_record_stores_values_correctly() -> None:
    """
    Ensure that LogRecord correctly stores and returns all provided values.
    This test verifies:
    - All constructor arguments are preserved
    - Getter methods return the exact same objects/values
    """
    record = LogRecord(
        notification_id = 1,
        date=datetime(2024, 1, 1, 12, 0),
        subject="Test Subject",
        message="Hello World",
        sender="Alice Smith",
        recipients=5
    )

    assert record.get_notification_id() == 1
    assert record.get_date() == datetime(2024, 1, 1, 12, 0)
    assert record.get_subject() == "Test Subject"
    assert record.get_message() == "Hello World"
    assert record.get_sender() == "Alice Smith"
    assert record.get_recipients() == 5

def test_log_record_handles_none_values() -> None:
    """
    LogRecord should gracefully accept None for any field.

    This is important because database rows or external inputs may
    legitimately contain missing values.
    """
    record = LogRecord(
        notification_id=None,
        date=None,
        subject=None,
        message=None,
        sender=None,
        recipients=None
    )

    assert record.get_notification_id() is None
    assert record.get_date() is None
    assert record.get_subject() is None
    assert record.get_message() is None
    assert record.get_sender() is None
    assert record.get_recipients() is None