#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:notification_log.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: GUI for notification log search and review.

# Local Imports
from app.logic.models.LogRecord import LogRecord

# Python Imports
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
from typing import Any

class NotificationLog:
    """
    GUI component for viewing and filtering notification logs.
    Provides date filters, a results table, and navigation controls.
    """
    def __init__(
            self,
            parent: Any,
            app_context: Any
    ) -> None:
        """
        Initializes the notification log GUI

        Parameters:
            parent (Any): Parent GUI object
            app_context (Any): Shared application context
        """
        self.parent = parent
        self.app_context = app_context

        # Main container frame
        self.frame = tk.Frame(parent.root)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        # Top-level layout frame
        top_level = ttk.Frame(self.frame, padding=10)
        top_level.grid(column=0, row=0, sticky="nsew")
        top_level.columnconfigure(0, weight=1)
        top_level.rowconfigure(3, weight=1)

        # Header
        header_label = ttk.Label(top_level, text="Notification Logs", font=("Arial", 20, "bold"))
        header_label.grid(column=0, row=0, pady=(0, 10), sticky="n")

        # Instructions
        instruction_text = ("Using the date selectors below, select a date range to filter the "
                            "notification logs. Click Search to apply the filters, or Clear "
                            "to reset all filters.")

        header_memo = tk.Message(top_level, text = instruction_text, width=600)
        header_memo.grid(column=0, row=1, sticky="n")

        # Input section (date filters + buttons)
        input_frame = ttk.Frame(top_level, padding=10)
        input_frame.grid(column=0, row=2, sticky="ew")
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=1)

        # Start date
        sdate_label = ttk.Label(input_frame, text="Start Date: ")
        sdate_label.grid(column=0, row=0, sticky="e", padx=5)
        self.startdate_entry = DateEntry(input_frame, width=10, date_pattern="MM-dd-yyyy")
        self.startdate_entry.grid(column=1, row=0, sticky="w", padx=5)

        # End date
        edate_label = ttk.Label(input_frame, text="End Date: ")
        edate_label.grid(column=2, row=0, sticky="e", padx=5)
        self.enddate_entry = DateEntry(input_frame, width=10, date_pattern="MM-dd-yyyy")
        self.enddate_entry.grid(column=3, row=0, sticky="w", padx=5)

        # Buttons
        search_button = ttk.Button(input_frame, text="Search", command=self.search)
        search_button.grid(column=4, row=0)

        back_button = ttk.Button(input_frame, text="Back", command=self.back)
        back_button.grid(column=4, row=1)

        clear_button = ttk.Button(input_frame, text="Clear", command=self.clear)
        clear_button.grid(column=5, row=0)

        display_all_button = ttk.Button(input_frame, text="Display All", command=self.display_all)
        display_all_button.grid(column=5, row=1)

        # Table container
        tree_frame = ttk.Frame(top_level)
        tree_frame.grid(column=0, row=3, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Table setup
        self.tree = ttk.Treeview(tree_frame, columns=("date", "subject", "message",
                                                      "sender","recipients"), show="headings")
        self.tree.heading("date", text="Date/Time")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("message", text="Message")
        self.tree.heading("sender", text="Sender")
        self.tree.heading("recipients", text="Recipients")
        self.tree.grid(column=0, row=0, sticky="nsew")

        #Column widths
        self.tree.column("date", width=150, stretch=False)
        self.tree.column("subject", width=150, stretch=False)
        self.tree.column("message", width=400, stretch=True)
        self.tree.column("sender", width=100, stretch=False)
        self.tree.column("recipients", width=75, stretch=False)

        #Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(column=1, row=0, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.mainwindow = top_level

    def get_frame(self) -> tk.Frame:
        """
        Return the main frame for embedding
        """
        return self.frame

    def run(self) -> None:
        """
        Start the tkinter main loop for this window
        """
        self.mainwindow.mainloop()

    def clear(self) -> None:
        """
        Reset date filters and clear the results table
        """
        default = date.today()
        self.startdate_entry.set_date(default)
        self.enddate_entry.set_date(default)
        self.tree.delete(*self.tree.get_children())

    def back(self) -> None:
        """
        Navigate back to the database route
        """
        from app.GUI.utilities.routes import send_to_route
        send_to_route("dashboard", self.parent)

    def search(self) -> None:
        """
        Search the database for records
        """
        start = self.startdate_entry.get_date()
        end = self.enddate_entry.get_date()

        if end < start:
            messagebox.showerror("Invalid Date Range", "End date must be after start date")
            return

        self.tree.delete(*self.tree.get_children())

        try:
            all_data = LogRecord.search(start, end)
        except Exception as e:
            messagebox.showerror("Error: ", str(e))
            return

        for data in all_data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    data.get_date(),
                    data.get_subject(),
                    data.get_message(),
                    data.get_sender(),
                    data.get_recipients()
                )
            )

    def display_all(self) -> None:
        """
        Display all records
        """
        self.tree.delete(*self.tree.get_children())
        all_data = LogRecord.display_all()

        for data in all_data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    data.get_date(),
                    data.get_subject(),
                    data.get_message(),
                    data.get_sender(),
                    data.get_recipients()
                )
            )
