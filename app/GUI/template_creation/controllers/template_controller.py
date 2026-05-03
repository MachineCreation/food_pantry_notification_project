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
        self.parent = parent
        self.app_context = app_context
        self.view = TemplateView(parent, self)

    # Callbacks

    def on_save(self, event=None):
        """
        Handler for the Save Template button.
        """
        # Ask the view for the data
        template_name = self.view.get_template_name()

        # Perform Controller logic
        if not template_name.strip():
            messagebox.showerror("Validation Error", "Template Name cannot be empty.")
            return

        messagebox.showinfo("Success", f"Template '{template_name}' validated successfully!")
        print("Ready to hook up database insertion logic next sprint.")

    def on_cancel(self, event=None):
        """
        Handler for the Cancel button.
        """
        print("Closing application...")
        self.parent.quit()
