# -------------------------------------------------------------------------------
# filename: template_view.py
# Author: Lloyd Truong
# 2026-04-24
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------

from pathlib import Path
import pygubu


class TemplateView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.builder = pygubu.Builder()

        # Load the UI file
        ui_path = Path(__file__).parent / 'template.ui'
        self.builder.add_from_file(ui_path)

        # Extract the main frame and attach it to the parent window
        self.main_frame = self.builder.get_object('frame1', self.parent)

        # Connect button clicks directly to the Controller
        self.builder.connect_callbacks(self.controller)

    def set_default_tags(self, tags_list):
        """
        loads preset tag values into the Tags combobox
        :param tags_list: list of tag strings to display in the combobox
        """
        widget = self.builder.get_object("tags_combobox")
        widget["values"] = tags_list

    def set_existing_templates(self, template_names):
        """
        loads template names
        :param template_names: list of template names from the database
        """
        widget = self.builder.get_object("existing_templates_combobox")
        widget["values"] = template_names

    def get_template_name(self):
        """
        Helper method to get the text from the entry box.
        """
        # make sure entry1 matches the ID of the text box in your template.ui
        entry_widget = self.builder.get_object('entry1')
        return entry_widget.get()

    def get_subject(self):
        """
        Helper method to get the text from the entry box.
        """
        return self.builder.get_object("subject_entry").get()

    def get_tag_value(self):
        """
        Helper method to get the text from the entry box.
        """
        return self.builder.get_object("tags_combobox").get()

    def get_message(self):
        """
        Helper method to get the text from the entry box.
        """
        return self.builder.get_object("message_text").get("1.0", "end").strip()

    def get_selected_existing_template(self):
        """
        returns the currently selected template name from the Existing Templates dropdown
        """
        return self.builder.get_object("existing_templates_combobox").get()

    def set_template_name(self, value):
        """
        fills the Template Name field with the given value
        """
        widget = self.builder.get_object("entry1")
        widget.delete(0, "end")
        widget.insert(0, value)

    def set_subject(self, value):
        """
        fills the Subject field with the given value
        """
        widget = self.builder.get_object("subject_entry")
        widget.delete(0, "end")
        widget.insert(0, value)

    def set_tag_value(self, value):
        """
        sets the Tags combobox to the given value
        """
        widget = self.builder.get_object("tags_combobox")
        widget.set(value)

    def set_message(self, value):
        """
        fills the Message text box with the given value
        """
        widget = self.builder.get_object("message_text")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)

