# -------------------------------------------------------------------------------
# filename:app/GUI/GUI.py
# Author: Joseph Egan
# 2026-04-17
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: main GUI class for the Food Pantry Notification App

# Local imports
from app.gui.utilities.routes import send_to_route

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
            send_to_route("sign_in_up_choice", self)
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
    def show_route(self, route_class):
        '''
        shows the given route class frame
        '''
        self.clear_frame()
        screen = route_class(self, self.__app_context)
        self.__current_frame = screen.get_frame()

    def log_in(self):
        '''
        logs in the user and shows the dashboard frame
        '''
        from app.gui.utilities.routes import send_to_route

        self.clear_frame()
        self.__app_context['logged_user'] = 'user'  # move to logic layer
        self.__app_context['user_role'] = 'admin'  # move to logic layer
        send_to_route("dashboard", self)

    def log_out(self):
        '''
        logs out the user and shows the sign in/up choice frame
        '''
        from app.gui.utilities.routes import send_to_route

        self.clear_frame()
        self.__app_context['logged_user'] = None  # move to logic layer
        self.__app_context['user_role'] = None  # move to logic layer
        send_to_route("sign_in_up_choice", self)

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
