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
            username: str,
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
            authenticated, user_role = database.authenticate_user(
                username,
                password
                )

            if authenticated:
                app_context['user'] = User(username, user_role)
            return authenticated

        return False
