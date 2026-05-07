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
from typing import Tuple


class User():
    '''
    class for user data and authentication
    '''
    __username: str
    __role: str

    def __init__(
            self,
            username: str,
            role: str
            ):
        self.__username = username
        self.__role = role

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
    def role(self) -> str:
        '''
        get the user role
        :return: the user role
        '''
        return self.__role

# --------------------------------- static ---------------------------------
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
            authenticated, user_role, username = database.authenticate_user(
                id,
                password,
                id_type
                )

            if authenticated:
                app_context['user'] = User(username, user_role)
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
