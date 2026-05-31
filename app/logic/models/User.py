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
            role: str,
            last_login: datetime | None = None,
            notification_type: str | None = None,
            dashboard_view: List[str] | None = None
            ):
        self.__username = username
        self.__user__id = user_id
        self.__role = role
        self.__last_login = last_login
        self.__notification_type = notification_type
        self.__dashboard_view = dashboard_view

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
    def dashboard_view(self) -> List[str] | None:
        '''
        get the user's dashboard view
        :return: the user's dashboard view
        '''
        return self.__dashboard_view
    
# --------------------------------- METHODS --------------------------------
    def set_dashboard_types(
            self,
            database: object,
    ) -> None:
        '''
        sets dashboard_view, last_login, and notification_type properties
        from the database
        :param database: the database object to get the data from
        :return: None
        '''
        

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

            if authenticated:
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
                username.strip().lower().title(),
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

        '''
        from app.database.models.Database import Database
        database: Database = app_context['database']
        valid, result = database.get_notes()

        if valid:
            return result
        return ('error', 'notes now found')
