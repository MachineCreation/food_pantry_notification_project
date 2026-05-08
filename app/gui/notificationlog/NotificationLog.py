#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/gui/notificationlog/NotificationLog.py
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
from datetime import date, datetime, time
from typing import Any


class NotificationLog:
    """
    GUI component for viewing and filtering notification logs.

    Features:
    - Date range filtering
    - Display all records
    - Row selection to preview message contents
    - Navigation back to dashboard

    It does not perform database access directly, it delegates to LogRecord
    """
    def __init__(
            self,
            parent: Any,
            app_context: Any,
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
        top_level.rowconfigure(4, weight=1)

        # Header
        header_label = ttk.Label(top_level,
                                 text="Notification Logs",
                                 font=("Arial", 20, "bold")
                                 )
        header_label.grid(column=0, row=0, pady=(0, 10), sticky="n")

        # Instructions
        instruction_text = (
            "Using the date selectors below, select a date range to filter the"
            " notification logs. Click Search to apply the filters, or Clear "
            "to reset all filters."
        )

        header_memo = tk.Message(top_level, text=instruction_text, width=600)
        header_memo.grid(column=0, row=1, sticky="n")

        # Input section (date filters + buttons)
        input_frame = ttk.Frame(top_level, padding=10)
        input_frame.grid(column=0, row=2, sticky="ew")

        # Configure input frame columns
        for col in range(6):
            input_frame.columnconfigure(col, weight=0)
        input_frame.columnconfigure(3, weight=1)

        # ---Row 0: Date Fields and Buttons---------

        # Start date
        startdate_label = ttk.Label(input_frame, text="Start Date: ")
        startdate_label.grid(column=0, row=0, sticky="e", padx=(0, 5))
        self.startdate_entry = DateEntry(input_frame, width=10, date_pattern="MM-dd-yyyy")
        self.startdate_entry.grid(column=1, row=0, sticky="w", padx=(0,15))

        # End date
        enddate_label = ttk.Label(input_frame, text="End Date: ")
        enddate_label.grid(column=2, row=0, sticky="e", padx=(0,5))
        self.enddate_entry = DateEntry(input_frame, width=10, date_pattern="MM-dd-yyyy")
        self.enddate_entry.grid(column=3, row=0, sticky="w")

        # Search Button
        search_button = ttk.Button(input_frame, text="Search", command=self.search)
        search_button.grid(column=4, row=0, padx=5)

        # Back Button
        back_button = ttk.Button(input_frame, text="Back", command=self.back)
        back_button.grid(column=5, row=0, padx=5)

        # ---Row 1: Dropdown + Buttons---------

        # Dropdown label
        sender_label = ttk.Label(input_frame, text="Filter by Sender")
        sender_label.grid(column=0, row=1, sticky="e", padx=(0,5))

        # Dropdown variable
        self.sender_variable = tk.StringVar()

        # Dropdown widget
        self.sender_dropdown = ttk.Combobox(
            input_frame,
            textvariable=self.sender_variable,
            values=LogRecord.get_unique_senders(),
            state="readonly",
            width=15
        )
        self.sender_dropdown.grid(column=1, row=1, sticky="w", padx=(0,15))
        self.sender_dropdown.current(0)

        # Clear Button
        clear_button = ttk.Button(input_frame, text="Clear", command=self.clear)
        clear_button.grid(column=4, row=1, padx=5)

        # Display All Button
        display_all_button = ttk.Button(input_frame, text="Display All", command=self.display_all)
        display_all_button.grid(column=5, row=1, padx=5)

        # ---Row 3: TreeFrame for Notification Log

        # Table container
        tree_frame = ttk.Frame(top_level)
        tree_frame.grid(column=0, row=3, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        # Table setup
        self.tree = ttk.Treeview(
            tree_frame,
            columns=(
                "date",
                "subject",
                "message",
                "sender",
                "recipients"
            ),
            show="headings"
        )
        self.tree.heading("date", text="Date/Time")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("message", text="Message")
        self.tree.heading("sender", text="Sender")
        self.tree.heading("recipients", text="Recipients")
        self.tree.grid(column=0, row=0, sticky="nsew")
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Column widths
        self.tree.column("date", width=150, stretch=False)
        self.tree.column("subject", width=150, stretch=False)
        self.tree.column("message", width=400, stretch=True)
        self.tree.column("sender", width=100, stretch=False)
        self.tree.column("recipients", width=75, stretch=False)

        # Vertical Scrollbar
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        tree_scrollbar.grid(column=1, row=0, sticky="ns")
        self.tree.configure(yscrollcommand=tree_scrollbar.set)

        # ---Row 4: Message Display----------

        # Message Display Frame
        mess_frame = ttk.Frame(top_level)
        mess_frame.grid(column=0, row=4, sticky="nsew")
        mess_frame.columnconfigure(0, weight=1)
        mess_frame.rowconfigure(0, weight=1)

        # Message Display
        self.mess_display = tk.Text(mess_frame, height=6, wrap="word")
        self.mess_display.grid(column=0, row=0, sticky="nsew")

        # Vertical Scrollbar
        mess_scrollbar = ttk.Scrollbar(mess_frame, orient="vertical", command=self.mess_display.yview)
        mess_scrollbar.grid(column=1, row=0, sticky="ns")
        self.mess_display.configure(yscrollcommand=mess_scrollbar.set)

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
        Reset date filters, clear the results table, and clear the message preview area
        """
        default = date.today()
        self.startdate_entry.set_date(default)
        self.enddate_entry.set_date(default)
        self.tree.delete(*self.tree.get_children())
        self.mess_display.config(state="normal")
        self.mess_display.delete("1.0", tk.END)
        self.mess_display.config(state="disabled")
        self.sender_dropdown.current(0)

    def back(self) -> None:
        """
        Navigate back to the database route
        """
        from app.gui.utilities.routes import send_to_route
        send_to_route("dashboard", self.parent)

    def on_row_select(self, _event: tk.Event) -> None:
        """
        Displays notification contents when user clicks on record in tree view
        """
        selected = self.tree.selection()
        if  not selected:
            return

        blocks = []

        for item_id in selected:
            values = self.tree.item(item_id, "values")
            message_text = (f"Sender: {values[3]} \t Date Sent: {values[0]} \t Received By: {values[4]} \n"
                        f"Subject: {values[1]} \n"
                        f"Message: {values[2]}")
            blocks.append(message_text)

        final_text = "\n\n".join(blocks)

        self.mess_display.config(state="normal")
        self.mess_display.delete("1.0", tk.END)
        self.mess_display.insert(tk.END, final_text)
        self.mess_display.config(state="disabled")

    def search(self) -> None:
        """
        Search the database for records
        """
        start = datetime.combine(self.startdate_entry.get_date(), time.min)
        end = datetime.combine(self.enddate_entry.get_date(), time.max)
        sender = self.sender_variable.get()

        if start > end:
            messagebox.showerror("Invalid Date Range", "End date must be after start date")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)
        self.mess_display.config(state="normal")
        self.mess_display.delete("1.0", tk.END)
        self.mess_display.config(state="disabled")


        try:
            all_data = LogRecord.search(start, end, sender)
        except Exception as e:
            messagebox.showerror("Internal Error", "This feature cannot run on your "
                                                   "computer due to a missing or incompatible driver.")
            return

        if not all_data:
            self.tree.insert("",
                             tk.END,
                             values=("", "", "No Results", "", "")
                             )

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
        Retrieve and display all log records in the table.
        """
        self.clear()
        try:
            all_data = LogRecord.display_all()
        except Exception as e:
            messagebox.showerror(
                "Internal Error",
                "This feature cannot run due to a missing or incompatible database driver"
            )
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
