#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/utilities/models/FrameBase.py
# Author: Joseph Egan
# 2026-04-22
# Sources: 
# Contributors: 
# -------------------------------------------------------------------------------
# Description: 

# Local imports

# python imports
from tkinter import ttk
import tkinter
import pygubu


class FrameBase():
    '''
    base class for frames,
    '''

    _app_context: dict | None = None
    _gui: tkinter.Tk | None = None

    def __init__(
            self,
            gui,
            app_context: dict,
            file_path: str,
            frame_name: str
            ) -> None:
        from app.gui.GUI import GUI

        self.__gui: GUI = gui
        self.__app_context: dict = app_context

        self.__builder: pygubu.Builder = pygubu.Builder()
        self.__builder.add_from_file(file_path)

        self.__frame = self.__builder.get_object(
            frame_name,
            self.__gui.root
        )

    def get_frame(self) -> tkinter.Frame:
        '''
        get the frame object
        :return: the frame object
        '''
        return self.__frame

    def register_buttons(
            self,
            buttons:
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]]
            ) -> None:
        '''
        helper method to register a button with a command and styles
        :param buttons: dict of button names, commands, and styles
        :return: None
        '''
        for button_name, button_info in buttons.items():
            button: ttk.Button = self.__builder.get_object(
                button_name,
                self.__frame
            )

            if button_info['commands'] != []:
                for func, param in button_info['commands'].items():
                    button.configure(
                        command=lambda func=func,
                        param=param: func(*param))

            if button_info['styles'] != []:
                for style in button_info['styles']:
                    button.configure(style=style)

    def register_entries(
            self,
            entries:
            dict[str, dict[str, dict[callable, list[any]] | list[ttk.Style]]]
            ) -> None:

        for entry_name, entry_info in entries.items():
            entry: tkinter.Entry = self.__builder.get_object(
                entry_name,
                self.__frame
            )

            if entry_info['commands'] != []:
                for func, param in entry_info['commands'].items():
                    validate_command = (
                        self.__gui.root.register(
                            lambda func=func,
                            param=param: func(*param)),
                        "%P"
                    )

                    entry.configure(
                        validate="key",
                        validatecommand=validate_command
                    )

            if entry_info['styles'] != []:
                for style in entry_info['styles']:
                    entry.configure(style=style)

    def send_to_route(self, route_name: str):
        '''
        helper method to send to a route
        :param route_name: name of the route to send to
        :return: None
        '''
        from app.gui.utilities.routes import send_to_route

        send_to_route(route_name, self.__gui)
