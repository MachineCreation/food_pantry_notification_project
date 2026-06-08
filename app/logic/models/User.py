#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/logic/models/user.py
# Author: Joseph Egan
# 2026-04-23
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: class for user data and authentication

# Local imports
from app.logic.models.Notification import Notification

# python imports
from typing import Tuple, List
from datetime import datetime


class User():
    '''
    class for user data and authentication
    '''
    __username: str
    __role: str

    def __init__(
            self,
            username: str,
            user_id: int,
            role: int,
            last_login: datetime | None = None,
            notification_type: str | None = None,
            dashboard_notifications: List[Notification] | None = None
            ):
        self.__username = username
        self.__user__id = user_id
        self.__role = role
        self.__last_login = last_login
        self.__notification_type = notification_type
        self.__dashboard_notifications = dashboard_notifications

    # --------------------
    def log_out(self, app_context: dict) -> None:
        '''
        helper method to log out the user
        :return: None
        '''

        app_context['user'] = None
        del self

# --------------------------------- properties -------------------------------
    @property
    def username(self) -> str:
        '''
        get the username
        :return: the username
        '''
        return self.__username

    @property
    def user_id(self) -> int:
        '''
        get the user_id
        :return: user id
        '''
        return self.__user__id

    @property
    def role(self) -> str:
        '''
        get the user role
        :return: the user role
        '''
        return self.__role

    @property
    def last_login(self) -> datetime | None:
        '''
        get the last login time
        :return: the last login time
        '''
        return self.__last_login

    @property
    def notification_type(self) -> str | None:
        '''
        get the user's notification type
        :return: the user's notification type
        '''
        return self.__notification_type

    @property
    def dashboard_notifications(self) -> List[Notification] | None:
        '''
        get the user's dashboard notifications
        :return: the user's dashboard notifications
        '''
        return self.__dashboard_notifications

# --------------------------------- setters ---------------------------------
    @last_login.setter
    def last_login(self, value: datetime) -> None:
        '''
        set the last login time
        :param value: the last login time to set
        :return: None
        '''
        self.__last_login = value

    @notification_type.setter
    def notification_type(self, value: str) -> None:
        '''
        set the user's notification type
        :param value: the notification type to set
        :return: None
        '''
        self.__notification_type = value

    @dashboard_notifications.setter
    def dashboard_notifications(self, value: List[Notification]) -> None:
        '''
        set the user's dashboard notifications
        :param value: the dashboard notifications to set
        :return: None
        '''
        self.__dashboard_notifications = value

# --------------------------------- METHODS --------------------------------
    def set_dashboard_types(
            self,
            database: object,
    ) -> None:
        '''
        sets dashboard_notifications, last_login, and notification_type
            properties
        from the database
        :param database: the database object to get the data from
        :return: None
        '''
        from app.database.models.Database import Database
        db: Database = database

        try:
            ok, user_info = db.get_user_settings(self.user_id)
            if ok and user_info:
                self.dashboard_notifications = \
                    user_info['dashboard_notifications']
                self.last_login = user_info['last_login']
                self.notification_type = user_info['notification_type']
        except ValueError as e:
            print(f"Error setting dashboard types: {e}")

    # --------------------
    def remove_dashboard_notifications(
            self,
            selected_notifications: set[int],
            database: object
    ) -> None:
        '''
        removes a notification from the user's dashboard notifications
        :param selected_notifications: the ids of the notifications to remove
        :return: None
        '''

        from app.database.models.Database import Database
        db: Database = database

        success = db.remove_user_dashboard_notifications(
            self.user_id,
            selected_notifications
        )

        if success:
            self.dashboard_notifications = [
                notification for notification in self.dashboard_notifications
                if notification.notification_id not in selected_notifications
            ]

    # --------------------
    def add_phone_number(
            self,
            phone_number: str,
            database: object
    ) -> None:
        '''
        adds a phone number to the user's account
        :param phone_number: the phone number to add
        :param database: the database object to update the account in
        :return: None
        '''
        from app.database.models.Database import Database
        db: Database = database

        success = db.add_phone_number(self.user_id, phone_number)

        if success:
            print("Phone number added successfully.")
        else:
            print("Error adding phone number.")

    # --------------------
    def update_notification_type(
            self,
            notification_type: str,
            database: object
    ) -> None:
        '''
        updates the user's notification type
        :param notification_type: the notification type to set
        :param database: the database object to update the account in
        :return: None
        '''
        from app.database.models.Database import Database
        db: Database = database

        success = db.update_user_notification_type(
            self.user_id,
            notification_type
        )

        if success:
            print("Notification type updated successfully.")
        else:
            print("Error updating notification type.")
            
    # --------------------
    def lock_account(
            self,
            database: object
    ) -> None:
        '''
        locks the user's account
        :param database: the database object to update the account in
        :return: None
        '''
        from app.database.models.Database import Database
        db: Database = database

        success = db.lock_user_account(self.user_id)

        if success:
            print("Account locked successfully.")
        else:
            print("Error locking account.")

# --------------------------------- STATIC ---------------------------------
    @staticmethod
    def authenticate(
            password: str,
            id: str,
            id_type: str,
            app_context: dict
            ) -> bool:
        '''
        helper method to authenticate the user
        :return: True if authenticated, False otherwise
        '''
        from app.database.models.Database import Database
        # get the username and password from the app context

        database: Database = app_context['database']

        if database:
            authenticated, user_role, username, user_id = \
                database.authenticate_user(
                                            id,
                                            password,
                                            id_type
                                           )

            if authenticated and user_role != 0:
                app_context['user'] = User(username, user_id, user_role)
                return authenticated

        return False

    # --------------------
    @staticmethod
    def sign_up(
            first_name: str,
            last_name: str,
            username: str,
            email: str,
            password: str,
            campus: str,
            allergies: bool,
            app_context: dict
            ) -> bool:
        '''
        helper method to sign up the user
        :return: True if signed up, False otherwise
        '''
        from app.database.models.Database import Database
        # get the database from the app context

        database: Database = app_context['database']

        if database:
            signed_up = database.sign_up_user(
                username.strip().lower(),
                password,
                email.strip().lower(),
                first_name.strip().lower().title(),
                last_name.strip().lower().title(),
                allergies,
                campus
                )
            if signed_up:
                return signed_up

        return False

    # --------------------
    @staticmethod
    def get_notes(app_context: dict) -> Tuple[str]:
        '''
        Helper function deprecated in favor of set_dashboard_types.
        '''
        from app.database.models.Database import Database
        database: Database = app_context['database']
        valid, result = database.get_notes()

        if valid:
            return result
        return ('error', 'notes now found')

    # --------------------
    def update_last_login(
            self,
            database
    ) -> None:
        '''
        update the last_login field in user
        '''
        from app.database.models.Database import Database
        db: Database = database

        date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        db.update_last_login(
            self.user_id,
            date
        )
