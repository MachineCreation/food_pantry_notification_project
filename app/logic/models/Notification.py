#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:
# Author: Joseph Egan
# 2026-05-15
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: class that handles the sending and logging of notifications to
# subscribers

# Local imports
from app.database.models.Database import Database
from app.database.models.Notifier import Notifier

# python imports
from typing import List, Tuple
from datetime import datetime


class Notification():

    def __init__(
            self,
            sender_id: int,
            subject: str,
            message: str,
            template_id: int | None = None,
            image_id: int | None = None,
    ):
        self.__sender_id = sender_id
        self.__subject = subject
        self.__message = message
        self.__template_id = template_id
        self.__image_id = image_id
        self.__num_recipients: int | None = None
        self.__date: datetime | None = None

# ------------------------------- properties ---------------------------------
    @property
    def subject(self) -> str:
        '''
        get the subject of the notification
        :return: the subject of the notification
        '''
        return self.__subject

    @property
    def message(self) -> str:
        '''
        get the message of the notification
        :return: the message of the notification
        '''
        return self.__message

    @property
    def sender_id(self) -> int:
        '''
        get the sender id of the notification
        :return: the sender id of the notification
        '''
        return self.__sender_id

    @property
    def template_id(self) -> int | None:
        '''
        get the template id of the notification
        :return: the template id of the notification
        '''
        return self.__template_id

    @property
    def image_id(self) -> int | None:
        '''
        get the image id of the notification
        :return: the image id of the notification
        '''
        return self.__image_id

    @property
    def num_recipients(self) -> int | None: 
        '''
        get the number of recipients of the notification
        :return: the number of recipients of the notification
        '''
        return self.__num_recipients

    @property
    def date(self) -> datetime | None:
        '''
        get the date the notification was sent
        :return: the date the notification was sent
        '''
        return self.__date

    @property
    def notification_id(self) -> int | None:
        '''
        get the notification id
        :return: the notification id
        '''
        return self.__notification_id

    @property
    def is_new(self) -> bool | None:
        '''
        get whether the notification is new
        :return: whether the notification is new
        '''
        return self.__is_new

# --------------------------------- setters ---------------------------------
    @notification_id.setter
    def notification_id(self, value: int) -> None:
        '''
        set the notification id
        :param value: the notification id to set
        :return: None
        '''
        self.__notification_id = value

    @num_recipients.setter
    def num_recipients(self, value: int) -> None:
        '''
        set the number of recipients of the notification
        :param value: the number of recipients to set
        :return: None
        '''
        self.__num_recipients = value

    @date.setter
    def date(self, value: datetime) -> None:
        '''
        set the date the notification was sent
        :param value: the date to set
        :return: None
        '''
        self.__date = value

    @is_new.setter
    def is_new(self, value: bool) -> None:
        '''
        set whether the notification is new
        :param value: whether the notification is new
        :return: None
        '''
        self.__is_new = value

# --------------------------------- methods -------------------------------
    def send_notification(
            self,
            app_context: dict
    ) -> bool:
        '''
        breaks up logic to send notifications and log them to notification logs
        :param subject: string subject of the notification
        :param message: string message content of the notification
        :param app_context: dictionary context of the application
        '''
        try:
            self.__date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            # assign variables
            database: Database = app_context['database']
            notifier = app_context['notifier']

            if not app_context['notifier']:
                notifier = app_context['notifier'] = Notifier()

            # get recipients from database
            recipients: List[Tuple[str, int, str]] = database.get_recipients()
            self.__num_recipients: int = len(recipients)

            # send notification
            for recipient in recipients:
                if recipient[2] in ['email', 'Both']:
                    sent = notifier.process_emails(
                        self.__date,
                        self.__subject,
                        self.__message,
                        recipient[0]
                    )

                if recipient[2] in ['sms', 'Both']:
                    sent = notifier.process_sms(
                        self.__subject,
                        self.__message,
                        recipient[1]
                    )

                if not sent:
                    raise ValueError('Emails not sent')

            # log notification
            database.log_notification(
                self.__date,
                self.__subject,
                self.__message,
                self.__sender_id,
                self.__num_recipients,
                self.__image_id,
                self.__template_id
            )
            return True

        except (ValueError or KeyError) as e:
            print('there was an error on Notification.send_notification, '
                  'time for some debugging, lucky you!\n'
                  f'{e}')
            return False

    # --------------------------------- STATIC -------------------------------
    @staticmethod
    def send_sms_otp(
            recipient: List[int, str]
    ) -> str:
        '''
        send sms otp messages to listed recipients using textbelt API
        :param recipient: a list containing recipient ids and their phone
            number
        :return: an otp
        '''

        otp = Notifier.send_SMS_otp(
            recipient
        )
        return otp
