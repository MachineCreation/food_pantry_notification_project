#! /usr/bin/env python3.14
# ----------------------------------------------------------------------------
# filename: app/GUI/utilities/EntryBehavior.py
# Author: Joseph Egan
# 2026-04-21
# Sources:
# Contributors:
# ----------------------------------------------------------------------------
# Description: class for entry data model, used to configure entry fields in
# the GUI forms

# Local imports
from app.gui.utilities.ToolTip import ToolTip

# python imports
import tkinter


class EntryBehavior:
    @staticmethod
    def attach(
            widget: tkinter.Widget,
            hover_text: str | None = None,
            focus_text: str | None = None
            ):
        if hover_text:
            hover_tool_tip = ToolTip(widget, hover_text)
            widget.bind("<Enter>", hover_tool_tip.show)
            widget.bind("<Leave>", hover_tool_tip.hide)

        if focus_text:
            focus_tool_tip = ToolTip(widget, focus_text)
            widget.bind("<FocusIn>", focus_tool_tip.show)
            widget.bind("<FocusOut>", focus_tool_tip.hide)

        return focus_tool_tip, hover_tool_tip
