#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:LogRecord.py
# Author: Justin Crump
# 2026-05-26
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