#! /urs/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/GUI/dashboard/models/DashBoard.py
# Author: Joseph Egan
# 2026-04-21
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class is an empty dashboard page

# Local imports

# python imports
from tkinter import ttk
import pygubu


class DashBoard():
    '''
    class for dashboard page, currently empty
    '''
    __app_context: dict | None = None
    __gui: object | None = None

    def __init__(self, gui, app_context: dict):
        from app.gui.GUI import GUI

        self.__gui: GUI = gui
        self.__app_context = app_context

        self.__builder = pygubu.Builder()
        self.__builder.add_from_file("app/gui/dashboard/ui/dashboard.ui")

        self.__frame = self.__builder.get_object(
            "DummyDashboard",
            self.__gui.root
            )

        self.configure_buttons()

    def configure_buttons(self):
        '''
        Configure buttons and their commands
        '''
        self.__back_button: ttk.Button = self.__builder.get_object(
            "back_button",
            self.__frame)

        self.__back_button.configure(
            command=self.__gui.show_sign_in_up_choice
            )

    def get_frame(self):
        return self.__frame
