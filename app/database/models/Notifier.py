#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/database/models/Notifier.py
# Author: Joseph Egan
# 2026-05-15
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class that handles sending notifications via email
# Note: later will send via sms as well

# Local imports

# python imports
from typing import List, Tuple
from datetime import datetime


class Notifier():

    def __init__(self):
        self.connect()

# --------------------------------- connections -------------------------------
    def connect(self):
        '''
        connect with the email provider
        :return connection: email provider connection
        '''
        self.__connection = "this is a connection"

# --------------------------------- methods ---------------------------------
    def send_emails(
            self,
            subject: str,
            message: str,
            recipients: List[str]
    ) -> Tuple[bool, datetime]:
        '''
        send emails to listed recipients
        :param subject: string subject of the email
        :param message: string message content of the email
        :param recipients: list of string email addresses to send the email to
        :return: boolean indicating success or failure of the email sending
            operation
        '''
        date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        try:
            if not self.__connection:
                self.connect()
            if not all([subject, message, recipients]):
                raise ValueError()

            return True, date

        except ValueError or KeyError:
            return False, None
