# -------------------------------------------------------------------------------
# filename: app/gui/dashboard/models/MessageSettings.py
# Author: Joseph Egan
# 2026-06-03
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: class to handle the change of user message preference settings

# Local imports
from app.gui.utilities.models.FrameBase import FrameBase
from app.logic.utilities.validation import validate_phone_number
from app.gui.utilities.EntryBehavior import EntryBehavior

# python imports
from tkinter import ttk
from tkinter.messagebox import showwarning


class MessageSettings(FrameBase):
    '''
    class to handle the change of user message preference settings
    '''

    def __init__(self, gui, app_context: dict):
        super().__init__(
            gui,
            app_context,
            "app/gui/dashboard/ui/message_settings.ui",
            "message_settings"
        )

        self.configure_buttons()
        self.configure_fields()
        self.configure_verification_feature()

    # -------------------- methods --------------------
    def configure_buttons(self):
        '''
        configure the buttons for the message settings frame
        '''

        self.__back_button = self._builder.get_object("back_button")
        self.__back_button.configure(
            command=lambda: self.send_to_route("dashboard")
        )

        self.__save_button = self._builder.get_object("save_button")
        self.__save_button.configure(
            command=self.save_settings
        )

        self.__clear_button = self._builder.get_object("clear_button")
        self.__clear_button.configure(
            command=self.clear_fields
        )

    # --------------------
    def configure_fields(self):
        '''
        configure the fields for the message settings frame
        '''
        self.__message_type_entry: ttk.Combobox = \
            self._builder.get_object("message_type_entry")
        self.__message_type_entry.bind(
            "<<ComboboxSelected>>",
            lambda e: self.on_message_type_change()
        )

        self.__phone_number_entry: ttk.Entry = \
            self._builder.get_object("phone_number_entry")

        pn_tool_tip = EntryBehavior.attach(
            self.__phone_number_entry,
            "Enter phone number: 1234567890",
            "Enter phone number with no spaces or special characters:\n"
            "1234567890"
        )

        self.__phone_number_entry.bind(
            "<FocusOut>",
            lambda e: (
                pn_tool_tip[0].hide(e),
                pn_tool_tip[1].hide(e),
                self.validate_phone_number(self.__phone_number_entry.get())
            )
        )

    # --------------------
    def configure_verification_feature(self):
        '''
        configure the verification feature for the message settings frame
        '''

        # verification code button
        self.__send_verification_button: ttk.Button = \
            self._builder.get_object("send_code_button")
        # self.__send_verification_button.configure(
        #     command=self.send_verification
        # )
        self.__send_verification_button.grid_remove()

        code_style = ttk.Style()
        code_style.configure(
            "Verification.TLabelframe",
            background="green",
            foreground="lightgreen"
        )
        code_style.configure(
            "Verification.TLabelframe.Label",
            font=("Arial", 12)
        )

        # verification code label frame
        self.__verification_label_frame: ttk.Labelframe = \
            self._builder.get_object("verification_label_frame")
        self.__verification_label_frame.configure(
            style="Verification.TLabelframe"
        )
        self.__verification_label_frame.grid_remove()

        # verification code entry
        self.__verification_code_entry: ttk.Entry = \
            self._builder.get_object("verification_code_entry")

    # --------------------
    def validate_phone_number(self, phone_number: str):
        '''
        validate the phone number input
        '''
        valid = validate_phone_number(phone_number)
        if not valid:
            self.__phone_number_entry.delete(0, 'end')
            showwarning(
                "Invalid Phone Number",
                f"Invalid phone number: {phone_number}"
            )
        else:
            self.__phone_number_entry.configure(foreground="black")
            self.__phone_number_entry.configure(state="disabled")
            self.__back_button.configure(state="disabled")

    # --------------------
    def on_message_type_change(self):
        '''
        handle the change of message type selection
        '''
        selected_type = self.__message_type_entry.get()
        if selected_type in ["SMS", "Both"]:
            self.__phone_number_entry.configure(state="normal")
            self.__send_verification_button.grid()
            self.__verification_label_frame.grid()
        else:
            self.__phone_number_entry.configure(state="disabled")
            self.__phone_number_entry.delete(0, 'end')
            self.__send_verification_button.grid_remove()
            self.__verification_label_frame.grid_remove()

    # --------------------
    def save_settings(self):
        '''
        save the settings to the database
        '''
        pass

    # --------------------
    def clear_fields(self):
        '''
        clear the fields in the message settings frame
        '''
        self.__message_type_entry.set("None")
        self.__phone_number_entry.delete(0, 'end')
        self.__phone_number_entry.configure(state="disabled")
