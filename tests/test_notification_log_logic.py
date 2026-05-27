#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:test_notification_log_logic
# Author: Justin Crump
# 2026-05-26
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Unit tests for NotificationLog.
# These tests validate:
# - Date formatting behavior
# - Sorting logic (case-insensitive)
# - Resetting sort indicators on the GUI tree widget


# Local Imports
from unittest.mock import MagicMock
from datetime import datetime
from app.gui.notification_log.NotificationLog import NotificationLog

# Python Imports
import pytest

@pytest.fixture
def gui() -> NotificationLog:
    """
    Create a lightweight fake NotificatioNLog instance
    with only the attributes needed for logic tests.
    """

    # Create an uninitialized instance
    gui = object.__new__(NotificationLog)

    # Minimal column definitions used by sorting/reset logic
    gui.columns = {
        "subject": ("Subject", 150),
        "date": ("Date", 150),
    }

    # Mock the tree widget to inspect calls
    gui.tree = MagicMock()
    return gui

def test_format_dt_with_datetime(gui: NotificationLog) -> None:
    """
    Ensure that a valid datetime object is formatted correctly.
    Expected format: DD-MM-YYYY HH:MM:SS
    """
    dt = datetime(2024, 1, 1, 15, 30)
    assert gui.format_dt(dt) == "01-01-2024 15:30:00"

def test_format_dt_invalid(gui: NotificationLog) -> None:
    """
    If the input is not a datetime, the method should return it unchanged
    """
    assert gui.format_dt("not a date") == "not a date"

def test_reset_sort_indicators(gui: NotificationLog) -> None:
    """
    reset_sort_indicators() should call tree.hading() once per column.
    This ensures that any sort arrows are cleared
    """
    gui.tree = MagicMock()
    gui.reset_sort_indicators()

    # One heading() call per column
    assert gui.tree.heading.call_count == len(gui.columns)

def test_sort_column_case_insensitive(gui: NotificationLog) -> None:
    """
    Verify that sorting is case-insensitive and stable.
    Expected order: alphabetical by subject
    """

    gui.tree = MagicMock()

    # Simulate 3 rows in the tree
    gui.tree.get_children.return_value = ["1", "2", "3"]

    # Mock the values stored in the "subject" column
    gui.tree.set.side_effect = lambda row, col: {
        "1": "apple",
        "2": "orange",
        "3": "red",
    }[row]

    gui.sort_column("subject", reverse=False)

    # Expected sorted order by subject
    expected_order = ["1", "2", "3"]

    # Extract the row IDs passed to the tree.set() during sorting
    moved = [call.args[0] for call in gui.tree.set.call_args_list]
    assert moved == expected_order