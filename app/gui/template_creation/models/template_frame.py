# -------------------------------------------------------------------------------
# filename: template_controller.py
# Author: Lloyd Truong
# 2026-05-23
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------


import tkinter as tk
from app.gui.utilities.models.FrameBase import FrameBase
from app.gui.template_creation.models.template_controller import TemplateController


class TemplateFrame(FrameBase):
    def __init__(self, gui, app_context):
        container = tk.Frame(gui.root)

        super().__init__(
            gui,
            app_context,
            frame=container
        )

        self._container = container
        self._controller = TemplateController(self._container, app_context, gui)

    def get_frame(self):
        return self._container

