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
from tkinter.messagebox import showwarning, showinfo


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

        self.__attempt_counter = 0
        self.configure_buttons()
        self.configure_fields()
        self.configure_verification_feature()
        self.get_note_type()
        self.on_message_type_change()

    # -------------------- methods --------------------
    def configure_buttons(self):
        '''
        configure the buttons for the message settings frame
        '''

        self.__back_button: ttk.Button = \
            self._builder.get_object("back_button")
        self.__back_button.configure(
            command=lambda: self.send_to_route("dashboard")
        )

        self.__save_button: ttk.Button = \
            self._builder.get_object("save_button")
        self.__save_button.configure(
            command=self.save_note_type
        )

        self.__verify_button: ttk.Button = \
            self._builder.get_object("verify_button")
        self.__verify_button.configure(
            command=self.verify_code
        )

        self.__clear_button: ttk.Button = \
            self._builder.get_object("clear_button")
        self.__clear_button.configure(
            command=self.clear_fields
        )

        self.__send_verification_button: ttk.Button = \
            self._builder.get_object("send_code_button")
        self.__send_verification_button.configure(
            command=self.send_verification
        )

        self.__verify_button: ttk.Button = \
            self._builder.get_object("verify_button")
        self.__verify_button.configure(
            command=self.verify_code
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
            "<Return>",
            lambda e: (
                pn_tool_tip[0].hide(e),
                pn_tool_tip[1].hide(e),
                self.validate_phone_number(self.__phone_number_entry.get())
            )
        )

        self.__verification_code_entry: ttk.Entry = \
            self._builder.get_object("verification_code_entry")
        self.__verification_code_entry.bind(
            "<KeyRelease>",
            lambda e: self.unlock_verify_button()
        )

    # --------------------
    def unlock_verify_button(self):
        '''
        unlock the verify button if the verification code entry is not empty
        '''
        if self.__verification_code_entry.get():
            self.__verify_button.configure(state="normal")
        else:
            self.__verify_button.configure(state="disabled")

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
        )
        code_style.configure(
            "Verification.TLabelframe.Label",
            font=("Arial", 12),
        )

        # verification code label frame
        self.__verification_label_frame: ttk.Labelframe = \
            self._builder.get_object("verification_label_frame")
        self.__verification_label_frame.configure(
            style="Verification.TLabelframe"
        )
        self.__verification_label_frame.grid_remove()

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
            self.__send_verification_button.grid()
            self.__verification_label_frame.grid()

    # --------------------
    def on_message_type_change(self):
        '''
        handle the change of message type selection
        '''
        selected_type = self.__message_type_entry.get()
        if selected_type in ["SMS", "Both"]:
            self.__phone_number_entry.configure(state="normal")
            self.__save_button.grid_remove()

        else:
            self.__phone_number_entry.configure(state="normal")
            self.__phone_number_entry.delete(0, 'end')
            self.__phone_number_entry.configure(state="disabled")
            self.__send_verification_button.grid_remove()
            self.__verification_label_frame.grid_remove()
            self.__save_button.grid()

    # --------------------
    def send_verification(self):
        '''
        send a verification code to the user's phone number
        '''
        from app.logic.models.Notification import Notification
        phone_number = int(self.__phone_number_entry.get())
        user_id = self._app_context['user'].user_id
        recipient = [user_id, phone_number]

        otp = Notification.send_sms_otp(
            recipient
        )

        if otp:
            showinfo(
                "Verification Code Sent",
                f"A verification code has been sent to {phone_number}."
            )
            self.__send_verification_button.configure(state="disabled")
            self.__otp = otp
            self._frame.after(300_000, self.handle_verification_timeout)

    # --------------------
    def handle_verification_timeout(self):
        '''
        handle the verification timeout by resetting the verification process
        '''
        if self.__otp is not None:
            showwarning(
                "Verification Timeout",
                "The verification code has expired. Please request a new code."
            )
            self.__attempt_counter += 1
            self.__otp = None
            self.__send_verification_button.configure(state="normal")
            self.__verification_code_entry.delete(0, 'end')

    # --------------------
    def verify_code(self):
        '''
        verify the code entered by the user
        '''
        try:
            valid = \
                bool(self.__otp == self.__verification_code_entry.get())
        except ValueError:
            valid = False

        if valid:
            showinfo(
                "Verification Successful",
                "Your phone number has been verified."
            )
            self.__verification_code_entry.delete(0, 'end')
            self.__verification_code_entry.configure(state="disabled")
            self.__send_verification_button.configure(state="disabled")
            self.__attempt_counter = 0
            self.__otp = None
            self._app_context['user'].\
                add_phone_number(
                    self.__phone_number_entry.get(),
                    self._app_context['database']
                )
            self._app_context['user'].update_notification_type(
                self.__message_type_entry.get(),
                self._app_context['database']
            )
            self.send_to_route("dashboard")

        else:
            self.__verification_code_entry.delete(0, 'end')
            showwarning(
                "Verification Failed",
                "The verification code you entered is incorrect. "
                "Please try again."
            )
            self.__attempt_counter += 1
            if self.__attempt_counter >= 3:
                showwarning(
                    "Too Many Attempts",
                    "You have entered an incorrect verification code too many"
                    " times. Please request a new code."
                )
                self.__attempt_counter = 0
                self.__otp = None
                self._app_context['user'].lock_account(
                    self._app_context['database']
                    )
                self._app_context['user'] = None
                self.send_to_route("sign_in")

    # --------------------
    def get_note_type(self):
        '''
        get the selected message type
        '''
        self.__message_type_entry.set(
            self._app_context['user'].notification_type
        )

    # --------------------
    def save_note_type(self) -> None:
        '''
        save the selected message type to the database
        '''
        selected_type = self.__message_type_entry.get()
        self._app_context['user'].update_notification_type(
            selected_type,
            self._app_context['database']
        )
        showinfo(
            "Notification Preference Updated",
            f"Your notification preference has been updated to {selected_type}"
            "."
        )
        self.send_to_route("dashboard")

    # --------------------
    def clear_fields(self):
        '''
        clear the fields in the message settings frame
        '''
        self.__message_type_entry.set("None")
        self.__phone_number_entry.delete(0, 'end')
        self.__phone_number_entry.configure(state="disabled")
