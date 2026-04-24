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

    @staticmethod
    def authenticate(
        gui,
        app_context: dict
        ) -> bool:
        '''
        helper method to authenticate the user
        :return: True if authenticated, False otherwise
        '''
        from app.database.models.Database import Database
        # get the username and password from the app context
        username: str = app_context['username']
        password: str = app_context['password']

        database: Database = app_context['database']

        if database:
            authenticated, user_role = database.authenticate_user(
                username,
                password
                )

            if authenticated:
                app_context['user_role'] = user_role
            return authenticated
        return False
