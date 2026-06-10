# -------------------------------------------------------------------------------
# filename: template_controller.py
# Author: Lloyd Truong
# 2026-04-24
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------

from tkinter import messagebox, filedialog
import os
import shutil
from pathlib import Path
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
        self.editing_existing_template = False
        self.view.set_title_text("Create Notification Template")
        self.view.set_save_button_text("Save Template")
        self.selected_image_path = None

        default_tags = [
            "Date",
            "Location",
            "Urgent Need",
            "Closure Notice",
            "Volunteer Request",
            "Restock Alert",
            "Holiday Hours",
            "General Update",
            "Image"
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
        image_path = self.selected_image_path

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
                image_path=image_path,
                creator_id=1
            )

            messagebox.showinfo("Success", f"Template '{template_name}' saved successfully!")
            self.load_existing_templates()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save template: {e}")

    def on_clear(self, event=None):
        """
        Clears all form fields in the Template Creation screen.
        Unlock template name
        Reset the page for creating new template
        """
        self.view.clear_form()
        self.editing_existing_template = False
        self.view.set_template_name_editable()
        self.view.set_title_text("Create Notification Template")
        self.view.set_save_button_text("Save Template")
        self.selected_image_path = None
        self.view.clear_image_path()
        self.view.text_images = []

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

            template_name, subject, tags, body_text, image_path = row

            self.editing_existing_template = True

            self.view.set_template_name(template_name)
            self.view.set_subject(subject)
            self.view.set_tag_value(tags)
            self.view.text_images = []
            self.view.set_message(body_text if body_text else "")

            self.selected_image_path = image_path
            if image_path:
                project_root = Path(__file__).resolve().parents[4]
                full_image_path = project_root / image_path

                if full_image_path.exists():
                    self.view.set_image_path(os.path.basename(image_path))
                    self.view.insert_image_into_message(str(full_image_path))
                else:
                    self.view.clear_image_path()
                    self.view.text_images = []
                    messagebox.showwarning("Missing Image", "The saved image file could not be found.")
            else:
                self.view.clear_image_path()
                self.view.text_images = []

            self.view.set_template_name_readonly()
            self.view.set_title_text("Edit Notification Template")
            self.view.set_save_button_text("Update Template")

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load template: {e}")

    def on_tag_selected(self, event=None):
        """
        inserts the selected tag into the message body when a tag is chosen
        """
        selected_tag = self.view.get_tag_value()
        if selected_tag.strip():
            if selected_tag == "Image":
                self.view.insert_tag_into_message("image")
            else:
                self.view.insert_tag_into_message(selected_tag)

    def on_delete_template(self, event=None):
        """
        deletes the selected existing template
        """
        selected_name = self.view.get_selected_existing_template()
        if not selected_name.strip():
            messagebox.showerror("Delete Error", "Please select a template first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete template '{selected_name}'?"
        )
        if not confirm:
            return

        try:
            self.logic.delete_template(selected_name)
            messagebox.showinfo("Success", f"Template '{selected_name}' deleted successfully!")

            self.view.clear_form()
            self.editing_existing_template = False
            self.view.set_template_name_editable()
            self.view.set_title_text("Create Notification Template")
            self.view.set_save_button_text("Save Template")
            self.load_existing_templates()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to delete template: {e}")

    def on_upload_image(self, event=None):
        """
        lets the admin choose an image file for the template
        copies it into the shared template images folder and
        saves the relative path
        """
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            project_root = Path(__file__).resolve().parents[4]
            images_folder = project_root / "app" / "gui" / "template_creation" / "images"
            images_folder.mkdir(parents=True, exist_ok=True)

            original_name = os.path.basename(file_path)
            destination_path = images_folder / original_name

            # avoid overwriting files with the same name
            counter = 1
            stem = destination_path.stem
            suffix = destination_path.suffix
            while destination_path.exists():
                destination_path = images_folder / f"{stem}_{counter}{suffix}"
                counter += 1

            shutil.copy(file_path, destination_path)

            relative_path = str(destination_path.relative_to(project_root))

            self.selected_image_path = relative_path
            self.view.set_image_path(os.path.basename(relative_path))
            self.view.insert_image_into_message(str(destination_path))

        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to upload image: {e}")

    def on_remove_image(self, event=None):
        """
        removes the selected image from the template
        """
        self.selected_image_path = None
        self.view.clear_image_path()
        current_message = self.view.get_message()
        self.view.set_message(current_message)
        self.view.text_images = []
        messagebox.showinfo("Image Removed", "The image was removed.")

