# -------------------------------------------------------------------------------
# filename: template_controller.py
# Author: Lloyd Truong
# 2026-04-24
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------

from tkinter import messagebox
from app.GUI.template_creation.views.template_view import TemplateView


class TemplateController:
    def __init__(self, parent, app_context):
        """
        Initializes the TemplateController
        :param parent: the parent tkinter window or frame
        :param app_context: shared application data
        """
        self.parent = parent
        self.app_context = app_context
        self.view = TemplateView(parent, self)
        self.db = self.app_context.get("database")

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
            rows = self.db.execute_query(
                "SELECT template_name FROM TEMPLATE ORDER BY template_name;",
                fetch_all=True
            )
            template_names = [row[0] for row in rows] if rows else []
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
            creator_id = 1

            self.db.execute_query(
                """
                INSERT INTO TEMPLATE (template_name, creator_id, subject, tags)
                VALUES (?, ?, ?, ?);
                """,
                (template_name, creator_id, subject, selected_tag),
                fetch_all=False
            )

            messagebox.showinfo("Success", f"Template '{template_name}' saved successfully!")
            self.load_existing_templates()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save template: {e}")

    def on_cancel(self, event=None):
        """
        Handler for the Cancel button.
        """
        print("Closing application...")
        self.parent.quit()
