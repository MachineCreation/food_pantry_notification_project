#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/GUI/utilities/ToolTip.py
# Author: Joseph Egan
# 2026-04-21
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: class to create tooltip text box in GUI

# Local imports

# python imports
import tkinter as tk


class ToolTip:
    def __init__(self, widget: tk.Widget, text: str):
        self.widget = widget
        self.text = text
        self.tip_window = None

    def show(self, _event: tk.Event):
        if self.tip_window or not self.text:
            return

        x = self.widget.winfo_rootx()
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        width = self.widget.winfo_width()

        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)

        label = tk.Label(
            self.tip_window,
            text=self.text,
            background="#bdbdbc",
            relief="solid",
            borderwidth=1,
            font=("Arial", 10),
            wraplength=width,
            justify="center",
        )

        label.pack(fill="both", expand=True)

        self.tip_window.update_idletasks()

        height = self.tip_window.winfo_reqheight()
        self.tip_window.wm_geometry(f"{width}x{height}+{x}+{y}")

    def hide(self, _event: tk.Event):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
