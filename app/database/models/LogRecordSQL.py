#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:LogRecordSQL.py
# Author: Justin Crump
# 2026-05-26
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: SQL for the Notification log GUI.

from app.database.models.Database import Database
from app.logic.models.LogRecord import LogRecord
from datetime import datetime
from typing import List

class LogRecordSQL:
    """
    Repository class responsible for retrieving notification log records
    from the database. This class isolates all SQL logic so the GUI
    layer does not interact with the database directly.
    """
    def __init__(self, db:Database) -> None:
        """
        Initialize the repository with a database connection.

        Parameters:
            db (Database): Database instance used to execute SQL queries
        """
        self.db = db

    def search(self, start_date: datetime, end_date: datetime, keyword: str) -> list[LogRecord]:
        """
        Search for notitfication records within a date range, optionally filtering
        by a keyword that may appear in the subject, body text, sender name, or
        sender username.

        Parameters:
            start_date (datetime): Beginning of the date range.
            end_date (datetime): End of the date range.
            keyword (str): Optional keyword for filtering.

        Returns:
            List[LogRecord]: List of matching notification records.
        """

        # Base query: Filter by date range
        query = """
            SELECT  NOTIFICATIONS.notification_id,
                    NOTIFICATIONS.date_time,
                    NOTIFICATIONS.subject,
                    NOTIFICATIONS.body_text,
                    USERS.first_name + ' ' + USERS.last_name AS full_name,
                    NOTIFICATIONS.num_recip
            FROM    NOTIFICATIONS
            LEFT OUTER JOIN USERS ON NOTIFICATIONS.sender_id = USERS.user_id
            WHERE   NOTIFICATIONS.date_time >= %s
            AND     NOTIFICATIONS.date_time <= %s
            """

        params = [start_date, end_date]

        # Add keyword filtering if provided
        if keyword:
            query += """
            AND (
                NOTIFICATIONS.subject LIKE %s
            OR  NOTIFICATIONS.body_text LIKE %s
            OR  USERS.first_name LIKE %s
            OR  USERS.last_name LIKE %s
            OR  (USERS.first_name + ' ' + USERS.last_name LIKE %s)
            OR  USERS.username LIKE %s)
            """
            pattern = f"%{keyword}%"
            params.extend([pattern]* 6)

        # Execute the query and fetch results
        rows = self.db.execute_query(query, tuple(params), fetch_all=True)

        # Convert raw SQL rows into LogRecord objects
        records = []
        for row in rows:
            record = LogRecord(
                notification_id=row[0],
                date=row[1],
                subject=row[2],
                message=row[3],
                sender=row[4],
                recipients=row[5],
            )
            records.append(record)
        return records

    def display_all(self) -> list[LogRecord]:
        """
        Retrieve all notification log records from the database.

        Returns:
            List[LogRecord]: List of matching notification records.
        """
        # Base Query: Returns all results
        query = """
        SELECT  NOTIFICATIONS.notification_id,
                NOTIFICATIONS.date_time,
                NOTIFICATIONS.subject,
                NOTIFICATIONS.body_text,
                USERS.first_name + ' ' + USERS.last_name AS full_name,
                NOTIFICATIONS.num_recip
        FROM    NOTIFICATIONS
        LEFT OUTER JOIN USERS ON NOTIFICATIONS.sender_id = USERS.user_id;
        """

        # Execute the query and fetch results
        rows = self.db.execute_query(query, fetch_all=True)

        # Convert raw SQL rows into LogRecord objects.
        records = []
        for row in rows:
            record = LogRecord(
                notification_id=row[0],
                date=row[1],
                subject=row[2],
                message=row[3],
                sender=row[4],
                recipients=row[5],
            )
            records.append(record)
        return records
