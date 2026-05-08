#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:LogRecord.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class and Logic for the notification log records

# Local Imports
from app.database.models.Database import Database

# Python Imports
from datetime import datetime
from typing import List


class LogRecord:
    """
    Represents a notification log entry retrieved from the database.
    """

    def __init__(
            self,
            notification_id: int,
            date: datetime,
            subject: str,
            message: str,
            sender: str,
            recipients: int
    ) -> None:
        """
        Initialize a LogRecord instance.

        Parameters:
        notification_id : int - Unique identifier for notification.
        date : datetime - The date the notification was sent.
        subject : str - Subject of the notification
        message : str - Body text of the notification
        sender : str - Notification sender's name or identifier
        recipients : int - Count of notification recipients
        """
        self.__notification_id: int = notification_id
        self.__date: datetime = date
        self.__subject: str = subject
        self.__message: str = message
        self.__sender: str = sender
        self.__recipients: int = recipients

    def get_notification_id(self) -> int:
        """Return the unique notification id"""
        return self.__notification_id

    def get_date(self) -> datetime:
        """Return the timestamp of the notification date"""
        return self.__date

    def get_subject(self) -> str:
        """Return the subject line of the notification"""
        return self.__subject

    def get_message(self) -> str:
        """Return the text body of the notification"""
        return self.__message

    def get_sender(self) -> str:
        """Return the sender's name or identifier"""
        return self.__sender

    def get_recipients(self) -> int:
        """Return the count of recipients that received the notification"""
        return self.__recipients

    @staticmethod
    def get_unique_senders():

        db = Database()
        query = """
        SELECT DISTINCT USERS.first_name + ' ' + USERS.last_name AS full_name
        FROM    USERS
        JOIN    ROLES ON USERS.role_id = ROLES.role_id
        WHERE   ROLES.role NOT LIKE '%subscriber%'
            """

        results = db.execute_query(query, fetch_all=True)

        users = ["All"]

        for user in results:
            username = user[0]
            users.append(username)
        return users

    @staticmethod
    def search(
        start_date: datetime,
        end_date: datetime,
        sender: str
    ) -> List["LogRecord"]:
        """
        Search for notification log records with a given date range

        Parameters:
            start_date : datetime - Start date of the search range
            end_date : datetime - End date of the search range
            sender : str = Username of the sender of the notification

        Returns:
            results : List[LogRecord] - List of LogRecord objects

        Raises:
            RuntimeError: If a database error occurs
        """

        db = Database()

        # Parameterized query to retrieve notification
        # details from the database
        query = """
        SELECT  NOTIFICATIONS.notification_id,
                NOTIFICATIONS.date_time,
                NOTIFICATIONS.subject,
                NOTIFICATIONS.body_text,
                USERS.first_name + ' ' + USERS.last_name AS full_name,
                NOTIFICATIONS.num_recip
        FROM    NOTIFICATIONS
        LEFT OUTER JOIN USERS ON NOTIFICATIONS.sender_id = USERS.user_id
        WHERE   NOTIFICATIONS.date_time >= ?
        AND     NOTIFICATIONS.date_time <= ?
        """

        # Base parameters
        params = [start_date, end_date]

        # Add sender filter only if needed
        if sender != "All":
            query += " AND (USERS.first_name + ' ' + USERS.last_name) LIKE ?"
            params.append(sender)
        else:
            query += ";"

        # Get all matching rows
        results = db.execute_query(query, tuple(params), fetch_all=True)

        # Build the list of LogRecord objects
        records = []
        for row in results:
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

    @staticmethod
    def display_all() -> List["LogRecord"]:
        """
        Display all notification records in the database

        Returns:
            List[LogRecord] - List of LogRecord objects
        """

        db = Database()

        query = """
        SELECT  NOTIFICATIONS.notification_id,
                NOTIFICATIONS.date_time,
                NOTIFICATIONS.subject,
                NOTIFICATIONS.body_text,
                USERS.first_name + ' ' + Users.last_name AS full_name,
                NOTIFICATIONS.num_recip
        FROM    NOTIFICATIONS
        LEFT OUTER JOIN USERS ON NOTIFICATIONS.sender_id = USERS.user_id;
        """

        # Fetch all matching rows
        results = db.execute_query(query, fetch_all=True)

        # Build the list of LogRecord objects
        records = []
        for row in results:
            record = LogRecord(
                notification_id=row[0],
                date=row[1],
                subject=row[2],
                message=row[3],
                sender=row[4],
                recipients=row[5]
            )
            records.append(record)
        return records
