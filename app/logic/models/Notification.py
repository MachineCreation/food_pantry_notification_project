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
from app.logic.models.User import User

# python imports
from typing import Tuple, List
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

    # --------------------------------- methods -------------------------------
    def send_notification(
            self,
            app_context: dict
    ):
        '''
        breaks up logic to send notifications and log them to notification logs
        :param subject: string subject of the notification
        :param message: string message content of the notification
        :param app_context: dictionary context of the application
        '''
        try:

            # assign variables
            database: Database = app_context['database']
            sender: User = app_context['user']

            if not app_context['notifier']:
                notifier = app_context['notifier'] = Notifier()

            # get recipients from database
            recipients: Tuple[str] = database.get_recipients()
            self.__num_recipients: int = len(recipients)

            # send notification
            sent, self.__date = notifier.send_emails(
                self.__subject,
                self.__message,
                self.__num_recipients
            )

            if not sent:
                raise ValueError('Emails not sent')

            # log notification
            database.log_notification(
                self.__date,
                self.__subject,
                self.__message,
                sender.user_id,
                self.__num_recipients,
                self.__image_id,
                self.__template_id
            )

        except (ValueError or KeyError) as e:
            print('there was an error on Notification.send_notificaation, time for some '
                  'debugging, lucky you!\n'
                  f'{e}')

    # --------------------

# --------------------------------- STATIC ---------------------------------
    @staticmethod
    def get_template_names(
            app_context: dict
    ) -> Tuple[str]:
        '''
        process a list of template names this should actually return a list of
            of template objects but there is no template object class
        :return: List of template names
        '''
        database: Database = app_context['database']

        if not database:
            print('database not found on Notification.get_template_names')

        try:
            names = database.get_template_names()
            if names == []:
                raise ValueError
            return names

        except ValueError:
            print('noting returned from database.get_template_names')

    # --------------------
    @staticmethod
    def get_template(
        name: str,
        app_context: dict
    ) -> Tuple[int, str, str] | None:
        '''
        call the database to get template details by name
        :param name: string name of template
        :param app_context: dict of app data
        :return: Tuple integer template_id, string template subject,
            string template message/body
        '''

        database: Database = app_context['database']

        try:
            valid, temp_id, subject, message = \
                database.get_template_by_name(name)

            if not valid:
                raise ValueError
            return temp_id, subject, message

        except ValueError:
            print(' not valid returned on Notification.get_template')

