# -------------------------------------------------------------------------------
# filename:GUI.py
# Author: Joseph Egan
# 2026-04-17
# Sources: 
# Contributors: 
# -------------------------------------------------------------------------------
# Description: main GUI class for the Food Pantry Notification App

# Local imports

# python imports
from tkinter import Tk

class GUI:
    '''
    Main GUI class for the Food Pantry Notification App.
    Responsible for creating and managing the tkinter GUI components.
    '''
    def __init__(self, root: Tk, app_context: dict):
        '''
        Initializes the GUI with the given tkinter root window.
        :param root: tkinter root window
        '''
        self.root = root
        #for future injection of shared app context ie database might not be needed
        self.app_context = app_context 
        self.create_widgets()

    def create_widgets(self):
        '''
        Creates and places the tkinter widgets in the GUI.
        '''
        pass
