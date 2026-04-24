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
            frame_name: str | None = None,
            frame: tkinter.Frame | None = None
            ) -> None:
        from app.gui.GUI import GUI

        self._gui: GUI = gui
        self._app_context: dict = app_context

        if not frame:
            self._builder: pygubu.Builder = pygubu.Builder()

            self._builder.add_from_file(file_path)

            self._frame = self._builder.get_object(
                frame_name,
                self._gui.root
            )
        else:
            self._frame = frame

    # --------------------
    def get_frame(self) -> tkinter.Frame:
        '''
        get the frame object
        :return: the frame object
        '''
        return self._frame

    # --------------------
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
            button: ttk.Button = self._builder.get_object(
                button_name,
                self._frame
            )

            if button_info['commands'] != []:
                for func, param in button_info['commands'].items():
                    button.configure(
                        command=lambda func=func,
                        param=param: func(*param))

            if button_info['styles'] != []:
                for style in button_info['styles']:
                    button.configure(style=style)

    # --------------------
    def send_to_route(self, route_name: str):
        '''
        helper method to send to a route
        :param route_name: name of the route to send to
        :return: None
        '''
        from app.gui.utilities.routes import send_to_route

        send_to_route(route_name, self._gui)
