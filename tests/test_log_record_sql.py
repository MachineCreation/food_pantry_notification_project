#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:test_log_record_sql
# Author: Justin Crump
# 2026-05-26
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Unit tests for LogRecordSQL.
# These tests validate:
# - Searching with and without keywords
# - Correct conversion of DB rows into LogRecord objects
# - Ensuring SQL parameter counts are correct
# - Displaying all log records

# Local Imports
from unittest.mock import MagicMock
from datetime import datetime
from app.database.models.LogRecordSQL import LogRecordSQL
from app.logic.models.LogRecord import LogRecord

# Python Imports
import pytest

@pytest.fixture
def mock_db() -> MagicMock:
    """
    Provide a MagicMock to simulate the database connection.
    """
    return MagicMock()

@pytest.fixture
def repo(mock_db: MagicMock) -> LogRecordSQL:
    """
    Create a LogRecordSQL repository using the mocked DB.
    """
    return LogRecordSQL(mock_db)

def test_search_without_keyword(repo: LogRecordSQL, mock_db: MagicMock) -> None:
    """
    Searching with an empty keyword should return all rows within the date range
    """
    mock_rows = [
        (1, datetime(2024, 1, 1), "Subject A", "Message A", "Alice SMith", 3),
        (2, datetime(2024, 1, 2), "Subject B", "Message B", "Bob JOnes", 5),
    ]

    mock_db.execute_query.return_value = mock_rows
    results = repo.search(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 31),
        keyword=""
    )

    assert len(results) == 2
    assert isinstance(results[0], LogRecord)
    assert results[0].get_subject() == "Subject A"

def test_search_with_keyword(repo: LogRecordSQL, mock_db: MagicMock) -> None:
    mock_rows = [
        (10, datetime(2024, 2, 1), "Hello", "World", "Alice Smith", 10)
        ]

    mock_db.execute_query.return_value = mock_rows

    results = repo.search(
        start_date=datetime(2024, 2, 1),
        end_date=datetime(2024, 3,1),
        keyword="Hello"
    )

    assert len(results) == 1
    assert results[0].get_message() == "World"


    # Extract the SQL parameters passed to execute_query()
    args, kwargs = mock_db.execute_query.call_args
    params = args[1]

    # The repostiory should pass 8 parameters for the keyword search
    assert len(params) == 8

def test_display_all(repo: LogRecordSQL, mock_db: MagicMock) -> None:
    """
    display_all() should return all rows as LogRecord objects.
    """
    mock_rows = [
        (5, datetime(2024, 3, 1), "X", "Y", "Z", 1)
    ]

    mock_db.execute_query.return_value = mock_rows
    results = repo.display_all()

    assert len(results) == 1
    assert results[0].get_sender() == "Z"