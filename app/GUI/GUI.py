# -------------------------------------------------------------------------------
# filename:GUI.py
# Author: Lloyd Truong
# 2026-04-23
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------
# Description: main GUI class for the Food Pantry Notification App

# Local imports
from app.GUI.template_creation.controllers.template_controller import TemplateController

# python imports
from tkinter import Tk


class GUI:
    """
    Main GUI class for the Food Pantry Notification App.
    Responsible for creating and managing the tkinter GUI components.
    """
    def __init__(self, root: Tk, app_context: dict):
        """
        Initializes the GUI with the given tkinter root window.
        :param root: tkinter root window
        """
        self.root = root
        self.app_context = app_context
        self.create_widgets()

    def create_widgets(self):
        """
        Creates and places the tkinter widgets in the GUI.
        """
        # Instantiate the Template Controller
        self.template_controller = TemplateController(self.root, self.app_context)

        # Pack/Grid the view's main frame onto the screen
        self.template_controller.view.main_frame.grid()
