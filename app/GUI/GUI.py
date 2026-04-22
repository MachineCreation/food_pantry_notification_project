# -------------------------------------------------------------------------------
# filename:app/GUI/GUI.py
# Author: Joseph Egan
# 2026-04-17
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: main GUI class for the Food Pantry Notification App

# Local imports
from app.gui.logInOut.models.SignInUpChoice import SignInUpChoice
from app.gui.logInOut.models.SignIn import SignIn
from app.gui.logInOut.models.SignUp import SignUp
from app.gui.dashboard.models.DashBoard import DashBoard

# python imports
import tkinter


class GUI:
    '''
    Main GUI class for the Food Pantry Notification App.
    Responsible for creating and managing the tkinter GUI components.
    '''
    __root: tkinter.Tk | None = None
    __app_context: dict = {
        'logged_user': None,
        'user_role': None
    }

    def __init__(self):
        '''
        Initialize the GUI, set up the root window, and show the initial frame.
        '''

        # set basic params for Tk root
        self.__root: tkinter.Tk = tkinter.Tk()
        self.__root.title("Food Pantry Notification App")
        self.__root.resizable(True, True)
        self.__root.grid()
        self.__root.anchor('center')
        self.__root.geometry("1000x700")
        self.__root.minsize(1000, 700)
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        self.__current_frame = None

        # show start frame
        if not self.__app_context['logged_user']:
            self.show_sign_in_up_choice()
        else:
            self.show_dashboard()

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

    def show_send_notification(self):
        '''
        shows the send notification frame
        '''
        self.clear_frame()
        pass

    def show_manage_users(self):
        '''
        shows the manage users frame
        '''
        self.clear_frame()
        pass

    def show_notification_log(self):
        '''
        shows the notification log frame
        '''
        self.clear_frame()
        pass

    def show_create_template(self):
        '''
        shows the create template frame
        '''
        self.clear_frame()
        pass

    def log_in(self):
        '''
        logs in the user and shows the dashboard frame
        '''
        self.clear_frame()
        self.__app_context['logged_user'] = 'user'  # move to logic layer
        self.__app_context['user_role'] = 'admin'  # move to logic layer
        self.show_dashboard()

    def log_out(self):
        '''
        logs out the user and shows the sign in/up choice frame
        '''
        self.clear_frame()
        self.__app_context['logged_user'] = None  # move to logic layer
        self.__app_context['user_role'] = None  # move to logic layer
        self.show_sign_in_up_choice()

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
