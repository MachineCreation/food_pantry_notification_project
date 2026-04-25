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
from app.gui.utilities.models.FrameBase import FrameBase
from app.logic.models.User import User
from app.logic.utilities.validation import input_string, non_empty_string, \
    is_email_or_username

# python imports
import tkinter
from tkinter import ttk
from tkinter.messagebox import showwarning


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
        self.register_entries()

    # --------------------
    def sign_in(self) -> None:
        '''
        helper method to sign in the user
        :return: None
        '''
        try:
            valid_uname_or_email, uname_email = input_string(
                self.__username_entry,
                is_email_or_username
                )

            if not valid_uname_or_email:
                showwarning(
                    "Invalid Input",
                    "Please enter a valid username or email."
                )

        except ValueError:
            showwarning(
                "Error",
                "An error occurred while validating the username or email."
            )
            self.clear_entries()
            return

        try:
            valid_password = input_string(
                self.__password_entry,
                non_empty_string
                )

            if not valid_password:
                showwarning(
                    "Invalid Input",
                    "Please enter a valid password."
                )
                self.clear_entries()
                return

        except ValueError:
            showwarning(
                "Error",
                "An error occurred while validating the password."
            )
            self.clear_entries()
            return

        authenticated: bool = User.authenticate(
            password=self.__password_entry.get(),
            id=self.__username_entry.get(),
            id_type=uname_email,
            app_context=self._app_context)

        if authenticated:
            self.send_to_route("dashboard")
        else:
            showwarning(
                "Authentication Failed",
                "Invalid username/email or password. Please try again."
            )
            self.clear_entries()

    # --------------------
    def register_entries(self) -> None:
        '''
        helper method to register and configure the entry fields for
            the frame
        :return: None
        '''
        # get and config username entry
        self.__username_entry: ttk.Entry = self._builder.get_object(
            "username_entry",
            self._frame
            )

        self.__username_entry.config(
            font=("Arial", 12),
        )

        # get and config password entry
        self.__password_entry: ttk.Entry = self._builder.get_object(
            "password_entry",
            self._frame
            )
        self.__password_entry.config(
            font=("Arial", 12),
            show="*",
            validate="focusout",
            validatecommand=(
                input_string(self.__password_entry, non_empty_string)
                )
        )

    # --------------------
    def clear_entries(self) -> None:
        '''
        helper method to clear the entry fields for the frame
        :return: None
        '''
        self.__username_entry.delete(0, tkinter.END)
        self.__password_entry.delete(0, tkinter.END)

# --------------------------------- properties ------------------------------
    @property
    def __buttons(self) -> \
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]]:
        '''
        helper method to get the buttons for the frame
        :return: dict of button names, commands, and styles
        '''
        ttk.Style().configure(
            "clear.TButton",
            background="#f9cf64"
        )
        buttons: \
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]] \
            = {
                "sign_in_button": {
                    "commands": {
                        self.sign_in: []
                        },
                    "styles": []
                },
                "sign_up_button": {
                    "commands": {
                        self. send_to_route: ["sign_up"]
                    },
                    "styles": []
                },
                "clear_button": {
                    "commands": {
                        self.clear_entries: []
                        },
                    "styles": ['clear.TButton']
                }
            }

        return buttons
