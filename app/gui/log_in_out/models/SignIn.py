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
from typing import Callable, Any


class SignIn(FrameBase):
    '''
    class for user sign in
    '''

    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/log_in_out/ui/sign_in.ui",
            "SignIn"
        )

        self.register_buttons(self.__buttons)
        self.register_entries()
        self._frame.bind_all(
            "<Return>",
            lambda e: self.sign_in()
        )
        self._frame.bind_all(
            "<KP_Enter>",
            lambda e: self.sign_in()
        )

    # --------------------
    def sign_in(self) -> None:
        '''
        helper method to sign in the user
        :return: None
        '''
        valid_uname_or_email, uname_email = self.__validate_username_or_email()
        valid_password = self.__validate_password()

        username_or_email = self.__username_entry.get()
        password = self.__password_entry.get()

        authenticated: bool = User.authenticate(
            password=password,
            id=username_or_email,
            id_type=str(uname_email),
            app_context=self._app_context)

        if not all([authenticated, valid_uname_or_email, valid_password]):
            showwarning(
                "Input Error",
                "Invalid username or password. "
                "Try again or contact your Administrator"
            )
            self.clear_entries()
            return

        self.send_to_route('dashboard')

    # --------------------
    def __validate_username_or_email(self) -> tuple[bool, str | None]:
        '''
        validate the username/email field and return its detected id type
        :return: (is_valid, id_type)
        '''
        try:
            valid_uname_or_email, uname_email = is_email_or_username(
                self.__username_entry.get()
            )

        except ValueError:
            showwarning(
                "Error",
                "An error occurred while processing your request."
            )
            self.clear_entries()
            return False, None

        if not valid_uname_or_email:
            self.clear_entries()
            return False, None

        return True, uname_email

    # --------------------
    def __validate_password(self) -> bool:
        '''
        validate the password field
        :return: True when valid, otherwise False
        '''
        try:
            valid_password = input_string(
                self.__password_entry,
                non_empty_string
            )

        except ValueError:
            showwarning(
                "Error",
                "An error occurred while processing your request."
            )
            self.clear_entries()
            return False

        if not valid_password:
            self.clear_entries()
            return False

        return True

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
        entry_font = ("Arial", 12)

        self.__username_entry.config(
            font=entry_font,
        )

        # get and config password entry
        self.__password_entry: ttk.Entry = self._builder.get_object(
            "password_entry",
            self._frame
            )
        self.__password_entry.config(
            font=entry_font,
            show="*"
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
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]]:
        '''
        helper method to get the buttons for the frame
        :return: dict of button names, commands, and styles
        '''
        ttk.Style().configure(
            "clear.TButton",
            background="#f9cf64"
        )
        buttons: \
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]] \
            = {
                "sign_in_button": {
                    "commands": {
                        self.sign_in: []
                        },
                    "styles": []
                },
                "sign_up_button": {
                    "commands": {
                        self.send_to_route: ["sign_up"]
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
