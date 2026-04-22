# -------------------------------------------------------------------------------
# filename:app/GUI/GUI.py
# Author: Joseph Egan
# 2026-04-17
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: main GUI class for the Food Pantry Notification App

# Local imports
from app.gui.logInOut.SignInUpChoice import SignInUpChoice
from app.gui.logInOut.SignIn import SignIn
from app.gui.logInOut.SignUp import SignUp
from app.gui.dashboard.models.DashBoard import DashBoard

# python imports
import tkinter


class GUI:
    '''
    Main GUI class for the Food Pantry Notification App.
    Responsible for creating and managing the tkinter GUI components.
    '''
    __root: tkinter.Tk | None = None
    __app_context: dict = {}

    def __init__(self, app_context):
        '''
        :param app_context: carries the data that will be fed to the rest of
            the app
            such as logged user.
        '''

        # set basic params for Tk root
        self.__root = tkinter.Tk()
        self.__root.title("Food Pantry Notification App")
        self.__root.resizable(True, True)
        self.__root.grid()
        self.__root.anchor('center')
        self.__root.geometry("1000x700")

        # set app context
        self.__app_context = app_context
        self.__current_frame = None

        # show start frame
        # if not self.__app_context['logged_user']:
        self.show_sign_in_up_choice()

    def clear_frame(self):
        if self.__current_frame:
            self.__current_frame.destroy()

# --------------------------------- properties -----------------------------
    @property
    def root(self):
        '''
        getter for the root Tkinter object
        '''
        return self.__root

# --------------------------------- Routes ---------------------------------
    def show_sign_in_up_choice(self):
        '''
        shows the sign in/up choice frame
        '''
        self.clear_frame()
        screen = SignInUpChoice(self, self.__app_context)
        self.__current_frame = screen.get_frame()

    def show_signin(self):
        '''
        shows the sign in frame
        '''
        self.clear_frame()
        screen = SignIn(self, self.__app_context)
        self.__current_frame = screen.get_frame()

    def show_signup(self):
        '''
        shows the sign up frame
        '''
        self.clear_frame()
        screen = SignUp(self, self.__app_context)
        self.__current_frame = screen.get_frame()

    def show_dashboard(self):
        '''
        shows the dashboard frame
        '''
        self.clear_frame()
        screen = DashBoard(self, self.__app_context)
        self.__current_frame = screen.get_frame()

# --------------------------------- run ---------------------------------
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
