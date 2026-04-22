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

# python imports
import tkinter
import pygubu


class SignIn():
    '''
    class for user sign in
    '''
    __app_context: dict | None = None
    __gui: tkinter.Tk | None = None

    def __init__(self, gui, app_context: dict):
        from app.gui.GUI import GUI

        self.__gui: GUI = gui
        self.__app_context = app_context

        self.__builder = pygubu.Builder()
        self.__builder.add_from_file("app/gui/logInOut/ui/sign_in.ui")

        self.__frame = self.__builder.get_object("SignIn", self.__gui.root)

        self.config_buttons()

    def config_buttons(self):
        '''
        Configure buttons and their commands
        '''

        # get buttons
        self.__sign_in_button = self.__builder.get_object(
            "sign_in_button",
            self.__frame)
        self.__sign_up_button = self.__builder.get_object(
            "sign_up_button",
            self.__frame)

        # bind to GUI navigation
        self.__sign_in_button.configure(
            command=self.__gui.log_in
            )
        self.__sign_up_button.configure(
            command=self.__gui.show_signup
            )

    def get_frame(self):
        return self.__frame
