#! /urs/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/GUI/dashboard/models/DashBoard.py
# Author: Joseph Egan
# 2026-04-21
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class is an empty dashboard page

# Local imports

# python imports
from tkinter import ttk
import tkinter
import pygubu


class DashBoard():
    '''
    class for dashboard page, currently empty
    '''
    __app_context: dict | None = None
    __gui: object | None = None

    def __init__(self, gui, app_context: dict):
        from app.gui.GUI import GUI

        self.__gui: GUI = gui
        self.__app_context: dict = app_context

        self.__builder: pygubu.Builder = pygubu.Builder()
        self.__builder.add_from_file("app/gui/dashboard/ui/dashboard.ui")

        self.__frame: ttk.Frame = self.__builder.get_object(
            "dashboard",
            self.__gui.root
            )

        self.__frame.configure()

        self.configure_buttons()
        self.configure_member_buttons(self.__app_context['user_role'])
        self.configure_admin_buttons(self.__app_context['user_role'])
        self.configure_text_area()

# --------------------------------- config ---------------------------------
    def configure_buttons(self):
        '''
        Configure buttons and their commands
        '''
        # logout button
        self.__log_out_button: ttk.Button = self.__builder.get_object(
            "log_out_button",
            self.__frame)
        log_out_style = ttk.Style()
        log_out_style.configure(
            "log_out.TButton",
            background="#f9cf64"
            )

        self.__log_out_button.configure(
            command=self.__gui.log_out,
            style="log_out.TButton"
            )

    def configure_member_buttons(self, role):
        '''
        configure buttons that are only visible to members, and admins
        '''

        self.__send_notification_button: ttk.Button = \
            self.__builder.get_object(
                "send_notification_button",
                self.__frame
            )
        self.__notification_log_button: ttk.Button = \
            self.__builder.get_object(
                "notification_log_button",
                self.__frame
            )

        if role == 'subscriber':
            self.__send_notification_button.destroy()
            self.__notification_log_button.destroy()

        else:
            self.__send_notification_button.configure(
                command=self.__gui.show_send_notification
                )
            self.__notification_log_button.configure(
                command=self.__gui.show_notification_log
            )

    def configure_admin_buttons(self, role):
        '''
        configure buttons that are only visible to admins
        '''
        self.__create_template_button: ttk.Button = \
            self.__builder.get_object(
                "create_template_button",
                self.__frame
            )
        self.__manage_users_button: ttk.Button = \
            self.__builder.get_object(
                "manage_users_button",
                self.__frame
            )

        if role != 'admin':
            self.__create_template_button.destroy()
            self.__manage_users_button.destroy()

        else:
            self.__create_template_button.configure(
                command=self.__gui.show_create_template
            )
            self.__manage_users_button.configure(
                command=self.__gui.show_manage_users
            )

    def configure_text_area(self):
        '''
        configure the text area for the dashboard
        '''
        # get notes widgets
        self.__recent_notes_frame: ttk.LabelFrame = self.__builder.get_object(
            "recent_notes_frame",
            self.__frame
        )
        self.__recent_notes_text: tkinter.Text = self.__builder.get_object(
            "recent_notes_text",
            self.__frame
        )
        self.__recent_notes_scroll: ttk.Scrollbar = self.__builder.get_object(
            "recent_notes_scroll",
            self.__frame
        )

        # bind scrollbar to text area
        self.__recent_notes_scroll.configure(
            command=self.__recent_notes_text.yview
        )
        self.__recent_notes_text.configure(
            yscrollcommand=self.__recent_notes_scroll.set
        )

        # configure notes widgets
        notes_style = ttk.Style()
        notes_style.configure(
            "notes.TLabelframe",
            borderwidth=2,
            relief="solid"
        )
        notes_style.configure(
            "notes.TLabelframe.Label",
            font=("Arial", 12)
        )

        self.__recent_notes_frame.configure(
            style="notes.TLabelframe"
        )
        self.__recent_notes_text.configure(
            state='disabled',
            font=("Arial", 12)
            )

    def get_frame(self):
        return self.__frame
