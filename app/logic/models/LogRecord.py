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
from app.Database.models.t_database import Database

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
        recipients : str - Count of notification recipients
        """
        self.__notification_id = notification_id
        self.__date = date
        self.__subject = subject
        self.__message = message
        self.__sender = sender
        self.__recipients = recipients

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
    def search(start_date: datetime, end_date: datetime) -> List["LogRecord"]:
        """
        Search for notification log records with a given date range

        Parameters:
            start_date : datetime - Start date of the search range
            end_date : datetime - End date of the search range

        Returns:
            List[LogRecord] - List of LogRecord objects
        """
        # Establish a database connection
        with Database.connect() as conn:
            cursor = conn.cursor()

        # Parameterized query to retrieve notification details from the database
        query = """
        SELECT  NOTIFICATIONS.notification_id,
                NOTIFICATIONS.date_time,
                NOTIFICATIONS.subject,
                NOTIFICATIONS.body_text,
                USERS.username,
                NOTIFICATIONS.num_recip
        FROM    NOTIFICATIONS
        LEFT OUTER JOIN USERS ON NOTIFICATIONS.sender_id = USERS.user_id
        WHERE   NOTIFICATIONS.date_time >= ?
        AND     NOTIFICATIONS.date_time <= ?;
        """
        cursor.execute(query, (start_date, end_date))

        # Get all matching rows
        results = cursor.fetchall()
        log_list = []

        # Convert each row into a LogRecord instance
        for row in results:
            log = LogRecord(
                notification_id=row[0],
                date=row[1],
                subject=row[2],
                message=row[3],
                sender=row[4],
                recipients=row[5])
            log_list.append(log)

        return log_list

    @staticmethod
    def display_all() -> List["LogRecord"]:
        """
        Display all notification records in the database

        Returns:
            List[LogRecord] - List of LogRecord objects
        """

        # Establish database connection
        with Database.connect() as conn:
            cursor = conn.cursor()

        query = """
        SELECT  NOTIFICATIONS.notification_id,
                NOTIFICATIONS.date_time,
                NOTIFICATIONS.subject,
                NOTIFICATIONS.body_text,
                USERS.username,
                NOTIFICATIONS.num_recip
        FROM    NOTIFICATIONS
        LEFT OUTER JOIN USERS ON NOTIFICATIONS.sender_id = USERS.user_id;
        """
        cursor.execute(query)

        # Fetch all matching rows
        results = cursor.fetchall()
        log_list = []

        # Convert each row into a LogRecord instance.
        for row in results:
            log = LogRecord(
                notification_id=row[0],
                date=row[1],
                subject=row[2],
                message=row[3],
                sender=row[4],
                recipients=row[5])
            log_list.append(log)

        return log_list