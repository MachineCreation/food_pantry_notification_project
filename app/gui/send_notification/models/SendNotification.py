#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/send_notification/models/SendNotification.py
# Author: Joseph Egan
# 2026-05-08
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: stand in class for send notification frame

# Local imports
from app.gui.utilities.models.FrameBase import FrameBase
from app.logic.models.Notification import Notification
from app.logic.utilities.validation import non_empty_string
from app.logic.models.Template import Template

# python imports
from typing import Callable, Any
from tkinter import ttk
from tkinter.messagebox import showwarning
import tkinter


class SendNotification(FrameBase):
    '''
    stand in class for send notification frame
    '''
    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/send_notification/ui/send_notification.ui",
            "send_notification"
        )
        self.__template_id: int | None = None
        self.__image_id: int | None = None
        self.__template_names = \
            list(Template.all_templates().keys())
        self.register_buttons(self.__buttons)
        self.register_entries()

    # --------------------------------- methods -------------------------------
    def send_notification(self) -> None:
        '''
        call send notification Logic
        '''
        print('send notification button pushed by'
              f' {self._app_context['user'].username}')

        non_empty_inputs = [
            non_empty_string(self.__message_entry.get(1.0, tkinter.END))[0],
            non_empty_string(self.__subject_entry.get())[0]
        ]

        if not all(non_empty_inputs):
            showwarning(
                "Input Error",
                "subject and message must have text"
            )
            return

        notification: Notification = Notification(
            self._app_context['user'].user_id,
            self.__subject_entry.get(),
            self.__message_entry.get(1.0, tkinter.END),
            self.__template_id,
            self.__image_id
        )

        notification.send_notification(self._app_context)

        self.clear_fields()

    # --------------------
    def populate_from_template(self) -> None:
        '''
        if a template is selected, populate the subject and message entries
        '''
        template: Template = Template.all_templates().get(self.__template_entry.get())

        self.__subject_entry.set(template.subject)
        self.__message_entry.delete(1.0, tkinter.END)
        self.__message_entry.insert(1.0, template.template_body)
        self.__template_id = template.template_id

    # --------------------
    def clear_fields(self) -> None:
        '''
        clear all registered fields
        '''
        self.__template_entry.set('')
        self.__subject_entry.set('')
        self.__message_entry.delete(1.0, tkinter.END)

    # --------------------
    def register_entries(self) -> None:
        '''
        register all notification entries
        '''
        self.__template_entry: ttk.Combobox = \
            self._builder.get_object(
                "template_entry",
                self._frame
            )
        self.__template_entry['values'] = self.__template_names
        self.__template_entry.bind(
            "<<ComboboxSelected>>",
            lambda e: self.populate_from_template()
        )

        self.__subject_entry: ttk.Combobox = \
            self._builder.get_object(
                "subject_entry",
                self._frame
            )

        self.__message_entry: tkinter.Text = \
            self._builder.get_object(
                "message_entry",
                self._frame
            )
        
        #  bind scrollbar
        self.__message_scroll: ttk.Scrollbar = \
            self._builder.get_object(
                "message_scroll",
                self._frame
            )
        self.__message_scroll.configure(
            command=self.__message_entry.yview
        )
        self.__message_entry.configure(
            yscrollcommand=self.__message_scroll.set,
        )

        # configure message widgets
        message_style = ttk.Style()
        message_style.configure(
            "message.TLabelframe",
            borderwidth=2,
            relief="solid"
        )
        message_style.configure(
            "message.TLabelframe.Label",
            font=("Arial", 12)
        )

        self.__message_frame: ttk.LabelFrame = \
            self._builder.get_object(
                "message_labelFrame",
                self._frame
            )

        self.__message_frame.configure(
            style="message.TLabelframe"
        )
        self.__message_entry.configure(
            font=("Arial", 12)
            )

    # ------------------------------- properties ------------------------------
    @property
    def __buttons(self) -> \
            dict[str, dict[str, dict[Callable, list[Any]] | list[str]]]:
        '''
        buttons for send notification frame
        '''
        return {
            "back_button": {
                "commands": {
                    self.send_to_route: ["dashboard"]
                },
                "styles": []
            },
            "send_button": {
                "commands": {
                    self.send_notification: []
                },
                "styles": []
            },
            "clear_button": {
                "commands": {
                    self.clear_fields: []
                },
                "styles": []
            },
        }
