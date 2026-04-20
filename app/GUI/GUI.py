# -------------------------------------------------------------------------------
# filename:app/GUI/GUI.py
# Author: Joseph Egan
# 2026-04-17
# Sources: 
# Contributors: 
# -------------------------------------------------------------------------------
# Description: main GUI class for the Food Pantry Notification App

# Local imports
# from app.GUI.LogInOut.SignInUpChoice import SignInUpChoice

# python imports
import tkinter
import pygubu

class GUI:
    '''
    Main GUI class for the Food Pantry Notification App.
    Responsible for creating and managing the tkinter GUI components.
    '''
    __root: tkinter.Tk | None = None
    __app_context: dict | None = None

    def __init__(self, app_context):
        '''
        :param app_context: carries the data that will be fed to the rest of the app
            such as logged user.
        '''

        # set basic params for Tk root
        self.__root = tkinter.Tk()
        self.__root.anchor('center')
        self.__root.geometry("1000x700")

        # set app context
        self.__app_context = app_context

        # set builder first panel
        self.__builder = pygubu.Builder()
        self.__builder.add_from_file("app/GUI/LogInOut/ui/signin_up_choice.ui")

        self.__main_frame = self.__builder.get_object("SignInUpChoice", self.__root)

    def run_gui(self):
        '''
        runs the main loop of the Gui object
        '''
        try:
            if self.__root:
                self.__root.mainloop()
            else:
                raise ValueError("Tkinter root not set")
        except ValueError as e:
            print(f'{e}')
