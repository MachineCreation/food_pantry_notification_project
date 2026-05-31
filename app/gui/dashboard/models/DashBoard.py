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
from app.gui.utilities.models.FrameBase import FrameBase
from app.logic.models.User import User
from app.logic.models.Template import Template

# python imports
from tkinter import ttk
import tkinter


class DashBoard(FrameBase):
    '''
    class for dashboard page, currently empty
    '''

    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/dashboard/ui/dashboard.ui",
            "dashboard"
            )

        # buttons in this class do not use the parent class's register buttons
        # method because they are too complicated so they are registered and
        # configured here
        self.configure_buttons()
        self.configure_member_buttons(self._app_context['user'].role)
        self.configure_admin_buttons(self._app_context['user'].role)
        self.configure_text_area()
        self.fill_template_app_context()

# --------------------------------- config ---------------------------------
    def configure_buttons(self):
        '''
        Configure buttons and their commands
        '''
        # logout button
        self.__log_out_button: ttk.Button = self._builder.get_object(
            "log_out_button",
            self._frame)
        log_out_style = ttk.Style()
        log_out_style.configure(
            "log_out.TButton",
            background="#f9cf64"
            )

        self.__log_out_button.configure(
            command=lambda: self.send_to_route("sign_in_up_choice"),
            style="log_out.TButton"
            )

    def configure_member_buttons(self, role):
        '''
        configure buttons that are only visible to members, and admins
        '''

        self.__send_notification_button: ttk.Button = \
            self._builder.get_object(
                "send_notification_button",
                self._frame
            )

        if role in [1, 0]:
            self.__send_notification_button.destroy()
            self.__notification_log_button.destroy()

        else:
            self.__send_notification_button.configure(
                command=lambda: self.send_to_route(
                    "send_notification"
                    )
                )

    def configure_admin_buttons(self, role):
        '''
        configure buttons that are only visible to admins
        '''
        self.__create_template_button: ttk.Button = \
            self._builder.get_object(
                "create_template_button",
                self._frame
            )
        self.__notification_log_button: ttk.Button = \
            self._builder.get_object(
                "notification_log_button",
                self._frame
            )
        self.__manage_settings_button: ttk.Button = \
            self._builder.get_object(
                "manage_settings_button",
                self._frame
            )

        if role != 3:
            self.__create_template_button.destroy()
            self.__manage_settings_button.destroy()
            self.__notification_log_button.destroy()

        else:
            self.__create_template_button.configure(
                command=lambda: self.send_to_route(
                    "create_template"
                    )
            )
            self.__manage_settings_button.configure(
                command=lambda: self.send_to_route(
                    "manage_settings"
                    )
            )
            self.__notification_log_button.configure(
                command=lambda: self.send_to_route(
                    "notification_log"
                    )
            )

    def configure_text_area(self):
        '''
        configure the text area for the dashboard
        '''
        # get notes widgets
        self.__recent_notes_frame: ttk.LabelFrame = self._builder.get_object(
            "recent_notes_frame",
            self._frame
        )
        self.__recent_notes_text: tkinter.Text = self._builder.get_object(
            "recent_notes_text",
            self._frame
        )
        self.__recent_notes_scroll: ttk.Scrollbar = self._builder.get_object(
            "recent_notes_scroll",
            self._frame
        )

        # get notes and configure for dashboard
        notes = User.get_notes(self._app_context)
        conf_notes = []
        if notes:
            for note in notes:
                conf_notes.append(
                    f"{note[0]}\n"
                    f"{note[1]}\n"
                    f"{note[2]}\n"
                    "\n--------------------\n\n"
                )

        conf_notes = "".join(conf_notes)

        # bind scrollbar to text area
        self.__recent_notes_scroll.configure(
            command=self.__recent_notes_text.yview
        )
        self.__recent_notes_text.configure(
            yscrollcommand=self.__recent_notes_scroll.set,
        )

        if conf_notes != '':
            self.__recent_notes_text.delete("1.0", "end")
            self.__recent_notes_text.insert("1.0", conf_notes)

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
        
    # --------------------
    def fill_template_app_context(self) -> None:
        '''
        conditionally get all templates from the database 
        '''
        
        role: int = self._app_context['user'].role

        if role not in [0, 1]:
            Template.get_all_templates(self._app_context['database'])

