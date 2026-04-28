# -------------------------------------------------------------------------------
# filename: app/GUI/LogInOut/SignInUpChoice.py
# Author: Joseph Egan
# 2026-04-17
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class for sign in/up choice

# Local imports
from app.gui.utilities.models.FrameBase import FrameBase

# python imports
from tkinter import ttk
from typing import Callable, Any


class SignInUpChoice(FrameBase):
    '''
    class for log in, sign up, and log out logic
    '''

    __app_context: dict | None = None
    __gui = None

    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/logInOut/ui/signin_up_choice.ui",
            "SignInUpChoice"
        )

        # configure frame attributes
        self.register_buttons(self.__buttons)

# --------------------------------- properties ------------------------------
    @property
    def __buttons(self) -> \
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]]:
        '''
        dict to carry
            <button name>: {
                'commands': [callable, ...],
                'styles': [ttk.Style, ...]
        }
        '''

        buttons: \
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]] \
            = {
                'sign_in_button': {
                    'commands': {self.send_to_route: ['sign_in']},
                    'styles': []
                },
                'sign_up_button': {
                    'commands': {self.send_to_route: ['sign_up']},
                    'styles': []
                },
            }

        return buttons
