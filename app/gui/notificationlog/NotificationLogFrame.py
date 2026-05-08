#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/notificationlog/NotificationLogFrame.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors: Joseph Egan
# -------------------------------------------------------------------------------
# Description:

# Local imports

# python imports

from app.gui.utilities.models.FrameBase import FrameBase
from app.gui.notificationlog.NotificationLog import NotificationLog


class NotificationLogFrame(FrameBase):
    """
    Wrapper that integrates the existing NotificationLog UI into the
    FrameBase routing
    """

    def __init__(self, gui, app_context):
        super().__init__(
            gui,
            app_context,
            None,
            "notification_log"
        )

        # Inject existing Tkinter UI into frame system
        self._ui = NotificationLog(self._frame, app_context)

    def get_frame(self):
        """
        Return the embedded frame so the FrameBase system can manage it
        """
        return self._ui.frame