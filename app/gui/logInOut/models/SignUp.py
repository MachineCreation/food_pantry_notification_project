#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/GUI/LogInOut/SignUp.py
# Author: Joseph Egan
# 2026-04-21
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class for user sign up

# Local imports
from app.gui.utilities.EntryBehavior import EntryBehavior
from app.gui.utilities.models.FrameBase import FrameBase
from app.logic.models.User import User
from app.logic.utilities.validation import is_valid_password, \
    validate_passwords_match, input_string, non_empty_string, \
    is_email_or_username

# python imports
from tkinter import ttk
from tkinter.messagebox import showwarning, showinfo
import tkinter
from typing import Callable, Any, Tuple


class SignUp(FrameBase):
    '''
    class for user sign up
    '''

    __campuses = [
        "Cascade",
        "Rock Creek",
        "Southeast",
        "Sylvania"
        ]

    __tooltips = []

    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/logInOut/ui/sign_up.ui",
            "SignUp")
        # config variables
        self.__allergies_bool = tkinter.BooleanVar()

        # config page
        self.register_buttons(self.__buttons)
        self.config_plain_entries()
        self.config_password_entries()
        self.config_campus_dropdown()
        self.config_allergies_checkbox()

        widgets = [
            self.__first_name_entry,
            self.__last_name_entry,
            self.__username_entry,
            self.__email_entry,
            self.__password_entry,
            self.__confirm_password_entry,
            self.__campus_entry,
        ]

        for idx, widget in enumerate(widgets):
            widget.bind(
                "<Tab>",
                lambda e, idx=idx: (widgets[(idx + 1) % len(widgets)]
                                    .focus_set(), "break")[1]
            )

    # --------------------
    def sign_up(self) -> None:
        '''
        run validation and sign up the user
        :return: None
        '''
        first_name, last_name, username, email, password, conf_pass, campus = \
            self.__required_values

        if not all(input_string(entry, non_empty_string)
                   for entry in self.__required_values):
            showwarning(
                "Invalid Input",
                "Please fill in all fields before signing up."
            )
            return

        signed_up = User.sign_up(
            first_name,
            last_name,
            username,
            email,
            password,
            campus,
            self.__allergies_bool.get(),
            self._app_context
        )

        if not signed_up:
            showwarning(
                "Sign Up Failed",
                "Try again or contact the Administrator"
            )
            self.clear_fields()
        else:
            showinfo(
                "Sign Up Successful",
                "Your account has been created. Please sign in."
            )
            self.clear_fields()
            # self.send_to_route("sign_in")

    # --------------------
    def show_password_mismatch(self, mismatch: bool) -> None:
        '''
        show a warning if the passwords do not match
        :param mismatch: whether the passwords do not match
        :return: None
        '''
        if mismatch is False and self.__confirm_password_entry.get() != '':
            showwarning(
                "Password Mismatch",
                "The passwords you entered do not match. Please try again."
            )
            self.__confirm_password_entry.delete(0, tkinter.END)

    # --------------------
    def show_passwords_valid(self, is_valid: bool) -> None:
        '''
        show a warning if the password is not valid
        :param is_valid: whether the password is valid
        :return: None
        '''
        if is_valid is False and self.__password_entry.get() != '':
            showwarning(
                "Invalid Password",
                "Password must be at least 8 characters. Please try again."
            )
            self.__password_entry.delete(0, tkinter.END)

    # --------------------
    def show_email_or_username_valid(self, valid: tuple[bool, str]) -> None:
        '''
        show a warning if the email or username is not valid
        :param valid: tuple of whether the input is valid and whether it is an
            email or username
        :return: None
        '''
        is_valid, pattern = valid
        if (is_valid is False or pattern != 'email') and \
                self.__email_entry.get() != '':
            showwarning(
                "Invalid Input",
                "Please enter a valid email"
            )
            self.__email_entry.delete(0, tkinter.END)

# --------------------------------- config ---------------------------------
    # --------------------
    def focus_next_widget(self, event):
        '''
        function to order tab events
        '''
        event.widget.tk_focusNext().focus()
        return "break"

    # --------------------
    def config_plain_entries(self):
        '''
        Entries that have no tool tips or special behavior can be
        configured here
        '''
        # get form fields
        self.__first_name_entry: ttk.Entry = \
            self._builder.get_object(
                "first_name_entry",
                self._frame)
        self.__last_name_entry: ttk.Entry = \
            self._builder.get_object(
                "last_name_entry",
                self._frame)
        self.__username_entry: ttk.Entry = \
            self._builder.get_object(
                "username_entry",
                self._frame)
        self.__email_entry: ttk.Entry = \
            self._builder.get_object(
                "email_entry",
                self._frame)
        self.__email_entry.bind(
            "<FocusOut>",
            lambda e: self.show_email_or_username_valid(
                is_email_or_username(self.__email_entry.get())
            )
        )

    # --------------------
    def config_password_entries(self):
        '''
        Configure password entry fields to hide input and add tool tips
        '''
        self.__password_entry: ttk.Entry = \
            self._builder.get_object(
                "password_entry",
                self._frame)
        pw_tool_tip = EntryBehavior.attach(
            self.__password_entry,
            "Enter password",
            "\nPassword must be at least 8 characters\n"
        )
        for tool_tip in pw_tool_tip:
            self.__tooltips.append(tool_tip)
        self.__password_entry.bind(
            "<Leave>",
            lambda e: (self.show_passwords_valid(
                is_valid_password(self.__password_entry.get())
                ), pw_tool_tip[0].hide(e), pw_tool_tip[1].hide(e))  # type: ignore
            )

        self.__confirm_password_entry: ttk.Entry = \
            self._builder.get_object(
                "confirm_password_entry",
                self._frame)
        cpw_tool_tip = EntryBehavior.attach(
            self.__confirm_password_entry,
            "Confirm password",
            "\nPassword fields must match\n"
        )
        for tool_tip in cpw_tool_tip:
            self.__tooltips.append(tool_tip)
        self.__confirm_password_entry.bind(
            "<FocusOut>",
            lambda e: (self.show_password_mismatch(
                validate_passwords_match(
                    self.__password_entry.get(),
                    self.__confirm_password_entry.get())
                ), cpw_tool_tip[0].hide(e), cpw_tool_tip[1].hide(e))  # type: ignore
            )

    # --------------------
    def config_campus_dropdown(self):
        '''
        Configure campus dropdown menu
        '''
        # configure campus dropdown
        self.__campus_entry: ttk.Combobox = \
            self._builder.get_object(
                "campus_entry",
                self._frame)
        self.__campus_entry['values'] = self.__campuses

    # --------------------
    def config_allergies_checkbox(self):
        '''
        Configure allergies checkbox
        '''
        # configure allergies checkbox
        style = ttk.Style()
        style.configure("Big.TCheckbutton", font=("Arial", 12))
        self.__allergies_entry: ttk.Checkbutton = \
            self._builder.get_object(
                "allergies_entry",
                self._frame)
        self.__allergies_entry.configure(
            variable=self.__allergies_bool,
            style="Big.TCheckbutton"
        )

    # --------------------
    def clear_fields(self):
        '''
        Clear all input fields in the sign-up form
        '''
        for entry in self.__clearable_entries:
            entry.delete(0, tkinter.END)
        self.__campus_entry.set('')
        self.__allergies_bool.set(False)

# ------------------------------ properties ---------------------------------
    @property
    def __required_values(self) -> Tuple[str, str, str, str, str, str]:
        '''
        helper method to get required sign-up form values
        :return: tuple of required form values
        '''
        return (
            self.__first_name_entry.get(),
            self.__last_name_entry.get(),
            self.__username_entry.get(),
            self.__email_entry.get(),
            self.__password_entry.get(),
            self.__confirm_password_entry.get(),
            self.__campus_entry.get()
        )

    @property
    def __clearable_entries(self) -> Tuple[ttk.Entry, ...]:
        '''
        helper method to get entries to clear
        :return: tuple of clearable entries
        '''
        return (
            self.__first_name_entry,
            self.__last_name_entry,
            self.__username_entry,
            self.__email_entry,
            self.__password_entry,
            self.__confirm_password_entry
        )

# --------------------------------- properties -------------------------------
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
                        self.send_to_route: ["sign_in"]
                        },
                    "styles": []
                },
                "sign_up_button": {
                    "commands": {
                        self.sign_up: []
                    },
                    "styles": []
                },
                "clear_button": {
                    "commands": {
                        self.clear_fields: []
                        },
                    "styles": ['clear.TButton']
                }
            }

        return buttons
