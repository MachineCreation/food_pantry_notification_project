# -------------------------------------------------------------------------------
# filename: template_controller.py
# Author: Lloyd Truong
# 2026-04-24
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------

from tkinter import messagebox
from app.gui.template_creation.models.template_view import TemplateView
from app.logic.models.Template_logic import TemplateLogic


class TemplateController:
    def __init__(self, parent, app_context, gui):
        """
        Initializes the TemplateController
        :param parent: the parent tkinter window or frame
        :param app_context: shared application data
        :param gui: main GUI object for routing/navigation
        """
        self.__parent = parent
        self.app_context = app_context
        self.gui = gui
        self.view = TemplateView(parent, self)
        self.db = self.app_context.get("database")
        self.logic = TemplateLogic(self.db)

        default_tags = [
            "Date",
            "Location",
            "Urgent Need",
            "Closure Notice",
            "Volunteer Request",
            "Restock Alert",
            "Holiday Hours",
            "General Update"
        ]
        self.view.set_default_tags(default_tags)
        self.load_existing_templates()

    def load_existing_templates(self):
        """
        reads existing template names from the database and loads them into the Existing Templates dropdown in the view
        """
        try:
            template_names = self.logic.get_existing_template_names()
            self.view.set_existing_templates(template_names)
        except Exception as e:
            print(f"Error loading existing templates: {e}")

    def on_save(self, event=None):
        """
        Handles the Save Template button action.
        :param event: optional tkinter event object
        """
        template_name = self.view.get_template_name()
        subject = self.view.get_subject()
        selected_tag = self.view.get_tag_value()
        message = self.view.get_message()

        if not template_name.strip():
            messagebox.showerror("Validation Error", "Template Name cannot be empty.")
            return
        if not subject.strip():
            messagebox.showerror("Validation Error", "Subject cannot be empty.")
            return
        if not selected_tag.strip():
            messagebox.showerror("Validation Error", "Tag cannot be empty.")
            return
        if not message.strip():
            messagebox.showerror("Validation Error", "Message cannot be empty.")
            return

        try:
            self.logic.save_template_and_message(
                template_name=template_name,
                subject=subject,
                tags=selected_tag,
                message=message,
                creator_id=1
            )

            messagebox.showinfo("Success", f"Template '{template_name}' saved successfully!")
            self.load_existing_templates()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save template: {e}")

    def on_clear(self, event=None):
        """
        Clears all form fields in the Template Creation screen.
        """
        self.view.clear_form()

    def on_back(self, event=None):
        """
        Goes back to the dashboard
        """
        from app.gui.utilities.routes import send_to_route
        send_to_route("dashboard", self.gui)

    def on_load_template(self, event=None):
        """
        Loads the selected template's information into the form fields.
        """
        selected_name = self.view.get_selected_existing_template()

        if not selected_name.strip():
            messagebox.showerror("Load Error", "Please select a template first.")
            return

        try:
            row = self.logic.get_template_details(selected_name)

            if not row:
                messagebox.showerror("Load Error", "Template not found.")
                return

            template_name, subject, tags, body_text = row

            self.view.set_template_name(template_name)
            self.view.set_subject(subject)
            self.view.set_tag_value(tags)
            self.view.set_message(body_text if body_text else "")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load template: {e}")

    def on_tag_selected(self, event=None):
        """
        inserts the selected tag into the message body when a tag is chosen
        """
        selected_tag = self.view.get_tag_value()
        if selected_tag.strip():
            self.view.insert_tag_into_message(selected_tag)

