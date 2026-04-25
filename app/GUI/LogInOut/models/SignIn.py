#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/GUI/LogInOut/SignIn.py
# Author: Joseph Egan
# 2026-04-21
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class for user sign in

# Local imports
from tkinter import ttk
from app.GUI.utilities.models.FrameBase import FrameBase
from app.logic.models.User import User

# python imports


class SignIn(FrameBase):
    '''
    class for user sign in
    '''

    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/logInOut/ui/sign_in.ui",
            "SignIn"
        )

        self.register_buttons(self.__buttons)
        self.register_entries(self.__entries)

    def sign_in(self, param: str) -> None:
        '''
        helper method to sign in the user
        :return: None
        '''
        authenticated: bool = User.authenticate(self.__gui, app_context=self.__app_context)
        print(param)
        self.send_to_route("dashboard")

# --------------------------------- properties ------------------------------
    @property
    def __buttons(self) -> \
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]]:
        '''
        helper method to get the buttons for the frame
        :return: dict of button names, commands, and styles
        '''
        buttons: \
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]] \
            = {
                "sign_in_button": {
                    "commands": {
                        self.sign_in: ['sign in button clicked']
                        },
                    "styles": []
                },
                "sign_up_button": {
                    "commands": {},
                    "styles": []
                }
            }

        return buttons

    @property
    def __entries(self) -> \
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]]:
        '''
        helper method to get the entries for the frame
        :return: dict of entry names, commands, and styles
        '''
        entries: \
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]] \
            = {
                "username_entry": {
                    "commands": [],
                    "styles": []
                },
                "password_entry": {
                    "commands": [],
                    "styles": []
                },
            }

        return entries
