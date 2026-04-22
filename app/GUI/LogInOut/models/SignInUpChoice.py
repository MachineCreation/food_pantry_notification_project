# -------------------------------------------------------------------------------
# filename: app/GUI/LogInOut/SignInUpChoice.py
# Author: Joseph Egan
# 2026-04-17
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class for sign in/up choice

# Local imports

# python imports
# import tkinter
import pygubu


class SignInUpChoice():
    '''
    class for log in, sign up, and log out logic
    '''

    __app_context: dict | None = None
    __gui = None

    def __init__(self, gui, app_context: dict):
        from app.gui.GUI import GUI

        self.__gui: GUI = gui
        self.__app_context = app_context

        self.__builder = pygubu.Builder()
        self.__builder.add_from_file("app/gui/logInOut/ui/signin_up_choice.ui")

        self.__frame = self.__builder.get_object(
            "SignInUpChoice",
            self.__gui.root
            )

        self.__frame.grid(row=0, column=0, sticky="nsew")
        self.config_buttons()

    def config_buttons(self):
        '''
        Configure buttons and their commands
        '''
        # get buttons
        self.__sign_in_button = self.__builder.get_object(
            "sign_in_button",
            self.__frame)
        self.__sign_up_button = self.__builder.get_object(
            "sign_up_button",
            self.__frame)

        # bind to GUI navigation
        self.__sign_in_button.configure(command=self.__gui.show_signin)
        self.__sign_up_button.configure(command=self.__gui.show_signup)

    def get_frame(self):
        return self.__frame
