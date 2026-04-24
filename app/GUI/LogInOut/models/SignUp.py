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
from app.gui.utilities.routes import send_to_route

# python imports
from tkinter import ttk
import tkinter
import pygubu


class SignUp():
    '''
    class for user sign up
    '''
    __app_context: dict | None = None
    __gui: tkinter.Tk | None = None
    __campuses = [
        "Cascade",
        "Rock Creek",
        "Southeast",
        "Sylvania"]

    def __init__(self, gui, app_context: dict):
        from app.gui.GUI import GUI

        self.__gui: GUI = gui
        self.__app_context = app_context
        self.__allergies_bool: tkinter.BooleanVar = \
            tkinter.BooleanVar(value=False)

        self.__builder = pygubu.Builder()
        self.__builder.add_from_file("app/gui/logInOut/ui/sign_up.ui")

        self.__frame = self.__builder.get_object("SignUp", self.__gui.root)

        # config page
        self.config_buttons()
        self.config_plain_entries()
        self.config_password_entries()
        self.config_campus_dropdown()
        self.config_allergies_checkbox()
        
    def config_buttons(self):
        '''
        Configure buttons and their commands
        '''
        # get buttons
        self.__sign_in_button: ttk.Button = self.__builder.get_object(
            "sign_in_button",
            self.__frame)
        self.__sign_up_button: ttk.Button = self.__builder.get_object(
            "sign_up_button",
            self.__frame)
        self.__clear_button: ttk.Button = self.__builder.get_object(
            "clear_button",
            self.__frame)

        # bind to GUI navigation
        self.__sign_in_button.configure(
            command=lambda: send_to_route("sign_in", self.__gui)
            )
        self.__sign_up_button.configure(
            command=self.__gui.log_in
            )

        # bind button functions
        self.__clear_button.configure(
            command=self.clear_fields
            )

    def config_plain_entries(self):
        '''
        Entries that have no tool tips or special behavior can be
        configured here
        '''
        # get form fields
        self.__first_name_entry: ttk.Entry = \
            self.__builder.get_object(
                "first_name_entry",
                self.__frame)
        self.__last_name_entry: ttk.Entry = \
            self.__builder.get_object(
                "last_name_entry",
                self.__frame)
        self.__username_entry: ttk.Entry = \
            self.__builder.get_object(
                "username_entry",
                self.__frame)
        self.__email_entry: ttk.Entry = \
            self.__builder.get_object(
                "email_entry",
                self.__frame)
        
    def config_password_entries(self):
        '''
        Configure password entry fields to hide input and add tool tips
        '''
        # configure password entries
        # TODO: add password validation and confirmation
        self.__password_entry: ttk.Entry = \
            self.__builder.get_object(
                "password_entry",
                self.__frame)
        EntryBehavior.attach(
            self.__password_entry,
            "Enter password",
            "\nPassword must be at least 8 characters\n"
        )

        self.__confirm_password_entry: ttk.Entry = \
            self.__builder.get_object(
                "confirm_password_entry",
                self.__frame)
        EntryBehavior.attach(
            self.__confirm_password_entry,
            "Confirm password",
            "\nPassword fields must match\n"
        )

    def config_campus_dropdown(self):
        '''
        Configure campus dropdown menu
        '''
        # configure campus dropdown
        self.__campus_entry: ttk.Combobox = \
            self.__builder.get_object(
                "campus_entry",
                self.__frame)
        self.__campus_entry['values'] = self.__campuses

    def config_allergies_checkbox(self):
        '''
        Configure allergies checkbox
        '''
        # configure allergies checkbox
        style = ttk.Style()
        style.configure("Big.TCheckbutton", font=("Arial", 12))
        self.__allergies_entry: ttk.Checkbutton = \
            self.__builder.get_object(
                "allergies_entry",
                self.__frame)
        self.__allergies_entry.configure(variable=self.__allergies_bool)
        self.__allergies_entry.configure(style="Big.TCheckbutton")

    def clear_fields(self):
        '''
        Clear all input fields in the sign-up form
        '''
        self.__first_name_entry.delete(0, tkinter.END)
        self.__last_name_entry.delete(0, tkinter.END)
        self.__username_entry.delete(0, tkinter.END)
        self.__email_entry.delete(0, tkinter.END)
        self.__password_entry.delete(0, tkinter.END)
        self.__confirm_password_entry.delete(0, tkinter.END)
        self.__campus_entry.set('')
        self.__allergies_bool.set(False)

    def get_frame(self):
        return self.__frame
