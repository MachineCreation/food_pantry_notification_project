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

    def get_template_name(self):
        """
        Helper method to get the text from the entry box.
        """
        # make sure entry1 matches the ID of the text box in your template.ui
        entry_widget = self.builder.get_object('entry1')
        return entry_widget.get()
