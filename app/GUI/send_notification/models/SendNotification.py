#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/send_notification/models/SendNotification.py
# Author: Joseph Egan
# 2026-05-08
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: stand in class for send notification frame

# Local imports
from app.gui.utilities.models.FrameBase import FrameBase

# python imports
from typing import Callable, Any


class SendNotification(FrameBase):
    '''
    stand in class for send notification frame
    '''
    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/send_notification/ui/send_notification.ui",
            "send_notification"
        )

        self.register_buttons(self.__buttons)

    # ------------------------------- properties ------------------------------
    @property
    def __buttons(self) -> \
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]]:
        '''
        buttons for send notification frame
        '''
        return {
            "back_button": {
                "commands": {
                    self.send_to_route: ["dashboard"]
                },
                "styles": []
            },
        }
