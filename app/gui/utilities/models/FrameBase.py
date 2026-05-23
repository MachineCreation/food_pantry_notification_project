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
from functools import partial
from tkinter import ttk
import tkinter
import pygubu
from typing import Callable, Any


class FrameBase():
    '''
    base class for frames,
    '''

    def __init__(
            self,
            gui,
            app_context: dict,
            file_path: str | None = None,
            frame_name: str | None = None,
            frame: tkinter.Frame | None = None
            ) -> None:
        from app.gui.GUI import GUI

        self._gui: GUI = gui
        self._app_context: dict = app_context

        if frame is None:
            if file_path is None or frame_name is None:
                raise ValueError(
                    "file_path and frame_name are required when frame is None"
                )

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
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]]
            ) -> None:
        '''
        helper method to register a button with a command and styles
        :param buttons: dict of button names, commands, and styles
        :return: None
        '''
        if self._builder is None:
            raise RuntimeError(
                "register_buttons requires a pygubu builder-backed frame"
            )

        for button_name, button_info in buttons.items():
            button: ttk.Button = self._builder.get_object(
                button_name,
                self._frame
            )

            button_config: dict[str, object] = {}

            commands = button_info.get('commands', {})
            if commands and isinstance(commands, dict):
                for func, param in commands.items():
                    button_config['command'] = partial(func, *param)

            styles = button_info.get('styles', [])
            if styles:
                for style in styles:
                    button_config['style'] = style

            button.configure(**button_config)

    # --------------------
    def send_to_route(self, route_name: str):
        '''
        helper method to send to a route
        :param route_name: name of the route to send to
        :return: None
        '''
        from app.gui.utilities.routes import send_to_route

        send_to_route(route_name, self._gui)  # type: ignore
