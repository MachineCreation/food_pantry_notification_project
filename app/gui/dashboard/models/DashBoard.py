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

        self.__selected_notifications = set()

        self.configure_buttons()
        self.configure_member_buttons(self._app_context['user'].role)
        self.configure_admin_buttons(self._app_context['user'].role)
        self._app_context['user']\
            .set_dashboard_types(self._app_context['database'])
        self.configure_text_area()
        self.fill_template_app_context()
        self._app_context['user']\
            .update_last_login(self._app_context['database'])

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
        
        self.__manage_settings_button: ttk.Button = self._builder.get_object(
            "manage_settings_button",
            self._frame
        )

        self.__manage_settings_button.configure(
            command=lambda: self.send_to_route(
                "message_settings"
                )
        )

        self.__clear_selection_button: ttk.Button = self._builder.get_object(
            "clear_selection_button",
            self._frame
        )

        self.__clear_selection_button.configure(
            command=self.clear_notification_selection
        )

        self.__remove_notification_button: ttk.Button = \
            self._builder.get_object(
                "remove_notification_button",
                self._frame
            )

        self.__remove_notification_button.configure(
            command=self.remove_selected_notifications
        )

        self.__update_notifications_button: ttk.Button = \
            self._builder.get_object(
                "update_notifications_button",
                self._frame
            )

        self.__update_notifications_button.configure(
            command=self.update_notifications
        )

    # --------------------
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

        else:
            self.__send_notification_button.configure(
                command=lambda: self.send_to_route(
                    "send_notification"
                    )
                )

    # --------------------
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

            self.__notification_log_button.configure(
                command=lambda: self.send_to_route(
                    "notification_log"
                    )
            )

    # --------------------
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
        # with orange new tag for new notifications
        notes = self._app_context["user"].dashboard_notifications
        # print(f'From dashboard.configure_text_area: {notes}')

        self.__recent_notes_text.configure(state="normal")
        self.__recent_notes_text.delete("1.0", "end")

        self.__recent_notes_text.tag_configure(
            "new_notification_tag",
            foreground="orange",
            font=("TkDefaultFont", 10, "bold")
        )

        self.__recent_notes_text.tag_configure(
            "selected_notification_tag",
            background="#d9eaff"
        )

        if notes:
            for note in notes:

                # create a unique tag for each notification to allow for
                # selection
                notification_tag = f"notification_{note.notification_id}"

                # start unique tag area
                start_index = self.__recent_notes_text.index("end-1c")

                if note.is_new:
                    self.__recent_notes_text.insert(
                        "end",
                        "NEW!\n",
                        "new_notification_tag"
                    )

                self.__recent_notes_text.insert(
                    "end",
                    f"{note.date}\n"
                    f"{note.subject}\n"
                    f"{note.message}\n"
                    "\n--------------------\n\n"
                )

                # end unique tag area
                end_index = self.__recent_notes_text.index("end-1c")

                self.__recent_notes_text.tag_add(
                    notification_tag,
                    start_index,
                    end_index
                )

                # bind click event to unique tag for selection
                self.__recent_notes_text.tag_bind(
                    notification_tag,
                    "<Button-1>",
                    lambda event,
                    selected_note=note: self.select_notification(
                        event,
                        selected_note
                    )
                )

        # bind scrollbar to text area
        self.__recent_notes_scroll.configure(
            command=self.__recent_notes_text.yview
        )
        self.__recent_notes_text.configure(
            yscrollcommand=self.__recent_notes_scroll.set,
            selectforeground="black",
            selectbackground="white"
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
        
    # --------------------
    def update_notifications(self) -> None:
        '''
        Update the notifications text area
        '''

        self._app_context['user']\
            .set_dashboard_types(self._app_context['database'])
        self.configure_text_area()

    # --------------------
    def select_notification(
            self,
            event: tkinter.Event,
            note: object
    ) -> str:
        """
        Select and highlight notifications
        """

        notification_id = note.notification_id
        notification_tag = f"notification_{notification_id}"

        # check if ctrl key is pressed during event
        ctrl_is_pressed = bool(event.state & 0x0004)

        self.__recent_notes_text.configure(state="normal")

        if not ctrl_is_pressed:
            self.__selected_notifications.clear()

            self.__recent_notes_text.tag_remove(
                "selected_notification_tag",
                "1.0",
                "end"
            )

        tag_ranges = self.__recent_notes_text.tag_ranges(notification_tag)

        if ctrl_is_pressed and notification_id in \
                self.__selected_notifications:
            self.__selected_notifications.remove(notification_id)

            if tag_ranges:
                self.__recent_notes_text.tag_remove(
                    "selected_notification_tag",
                    tag_ranges[0],
                    tag_ranges[1]
                )

            print(f"Unselected notification id: {notification_id}")

        else:
            self.__selected_notifications.add(notification_id)

            if tag_ranges:
                self.__recent_notes_text.tag_add(
                    "selected_notification_tag",
                    tag_ranges[0],
                    tag_ranges[1]
                )

            print(f"Selected notification id: {notification_id}")

        print(f"Currently selected: {self.__selected_notifications}")

        self.__recent_notes_text.tag_remove("sel", "1.0", "end")

        self.__recent_notes_text.configure(state="disabled")

        return

    # --------------------
    def fill_template_app_context(self) -> None:
        '''
        conditionally get all templates from the database
        '''

        role: int = self._app_context['user'].role

        if role not in [0, 1]:
            Template.get_all_templates(self._app_context['database'])

    # --------------------
    def clear_notification_selection(self) -> None:
        '''
        clear the current notification selection
        '''
        self.__selected_notifications.clear()
        self.__recent_notes_text.configure(state="normal")
        self.__recent_notes_text.tag_remove(
            "selected_notification_tag",
            "1.0",
            "end"
        )
        self.__recent_notes_text.tag_remove("sel", "1.0", "end")
        self.__recent_notes_text.configure(state="disabled")

    # --------------------
    def remove_selected_notifications(self) -> None:
        '''
        remove the selected notifications from the user's dashboard
        '''
        from app.logic.models.User import User
        user: User = self._app_context['user']
        if not self.__selected_notifications:
            return

        user.remove_dashboard_notifications(
            self.__selected_notifications,
            self._app_context['database']
        )

        self.clear_notification_selection()
        self.configure_text_area()
