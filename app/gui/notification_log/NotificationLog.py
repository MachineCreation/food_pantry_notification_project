#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:NotificationLog.py
# Author: Justin Crump
# 2026-05-26
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: GUI for notification log search and review.

# Local Imports
from app.database.models.LogRecordSQL import LogRecordSQL
from app.database.models.Database import Database

# Python Imports
import tkinter as tk
import tkinter.ttk as ttk
import csv
from tkcalendar import DateEntry
from tkinter import messagebox, filedialog
from datetime import date, datetime, time
from typing import Any

class NotificationLog:
    """
    GUI component for viewing and filtering notification logs.

    Features:
    - Date range filtering
    - Keyword filtering
    - Display all records
    - Row selection to preview message contents
    - Notification resend support
    - CSV export
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


        # Initializes the database
        self.repo = LogRecordSQL(Database())

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
        top_level.rowconfigure(5, weight=1)

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

        # Configure input frame columns
        for col in range(6):
            input_frame.columnconfigure(col, weight=0)
        input_frame.columnconfigure(3, weight=1)

        # ---Row 0: Date Fields and Buttons---------

        # Start date
        startdate_label = ttk.Label(input_frame, text="Start Date: ")
        startdate_label.grid(column=0, row=0, sticky="e", padx=(0,5))
        self.startdate_entry = DateEntry(input_frame, width=10, date_pattern="mm-dd-yyyy", state="readonly")
        self.startdate_entry.grid(column=1, row=0, sticky="w", padx=(0,15))

        # End date
        enddate_label = ttk.Label(input_frame, text="End Date: ")
        enddate_label.grid(column=2, row=0, sticky="e", padx=(0,5))
        self.enddate_entry = DateEntry(input_frame, width=10, date_pattern="mm-dd-yyyy", state="readonly")
        self.enddate_entry.grid(column=3, row=0, sticky="w")

        # Search Button
        search_button = ttk.Button(input_frame, text="Search", command=self.search)
        search_button.grid(column=4, row=0, padx=5)

        # Back Button
        back_button = ttk.Button(input_frame, text="Back", command=self.back)
        back_button.grid(column=5, row=0, padx=5)

        # ---Row 1: Dropdown + Buttons---------

        # Keyword variable
        self.keyword_variable = tk.StringVar()

        # Keyword Label
        keyword_label = ttk.Label(input_frame, text="Keyword Search: ")
        keyword_label.grid(column=0, row=1, sticky="e", padx=(10,5))

        # Keyword Entry
        self.keyword_entry = ttk.Entry(input_frame, textvariable=self.keyword_variable, width=20)
        self.keyword_entry.grid(column=1, row=1, sticky="w")

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
        self.columns = {
            "date": ("Date/Time", 150),
            "subject": ("Subject", 150),
            "message": ("Message", 400),
            "sender": ("Sender", 100),
            "recipients": ("Recipients", 75)
        }
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

        # Configure each Treeview column and attach sort handler
        for col, (title, width) in self.columns.items():
            self.tree.heading(col, text=title, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=width)

        # Place the treeview in the layout
        self.tree.grid(column=0, row=0, sticky="nsew")

        # Bind row-selection events
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

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
        self.mess_display.config(state="disabled")

        # Vertical Scrollbar
        mess_scrollbar = ttk.Scrollbar(mess_frame, orient="vertical", command=self.mess_display.yview)
        mess_scrollbar.grid(column=1, row=0, sticky="ns")
        self.mess_display.configure(yscrollcommand=mess_scrollbar.set)

        # ---Row 5: Notification Re-send and Export Buttons
        resend_frame = ttk.Frame(top_level)
        resend_frame.grid(column=0, row=5, sticky="e")
        resend_frame.columnconfigure(0, weight=0)
        resend_frame.rowconfigure(1, weight=0)

        # Resend Notification
        self.resend_button = ttk.Button(resend_frame, text="Resend", command=self.resend_notification, state="disabled")
        self.resend_button.grid(column=0, row=0, padx=5)

        # Export Notification Log
        export_button = ttk.Button(resend_frame, text="Export", command=self.export_csv)
        export_button.grid(column=1, row=0, padx=5)

        self.mainwindow = top_level

    def get_frame(self) -> tk.Frame:
        """
        Return the main frame for embedding
        """
        return self.frame

    def clear(self) -> None:
        """
        Reset date filters, clear the results table, clears sort order,
        and clear the message preview area
        """
        default = date.today()
        self.startdate_entry.set_date(default)
        self.enddate_entry.set_date(default)
        self.tree.delete(*self.tree.get_children())
        self.clear_message_display()
        self.keyword_entry.delete(0,tk.END)
        self.reset_sort_indicators()
        self.resend_button.config(state="disabled")

    def back(self) -> None:
        """
        Navigate back to the database route
        """
        from app.gui.utilities.routes import send_to_route
        send_to_route("dashboard", self.parent)

    def resend_notification(self) -> None:
        """
        Load the selected notification into the Send Notification page.
        """

        selected = self.tree.selection()

        if len(selected) == 0:
            messagebox.showwarning("No Selection", "Please select a notification to resend")
            return

        if len(selected) > 1:
            messagebox.showwarning("Multiple Selections", "Please select only one notification to resend.")
            return

        item_id = selected[0]
        values = self.tree.item(item_id, "values")

        # Current order: date, subject, message, sender, recipients
        self.app_context["resend_notification"] = {
            "subject": values[1],
            "message": values[2]
        }

        from app.gui.utilities.routes import send_to_route
        self.app_context["send_notification_return_route"] = "notification_log"
        send_to_route("send_notification", self.parent)

    def on_row_select(self, _event: tk.Event) -> None:
        """
        Displays notification contents when user clicks on record in tree view
        """
        # Get all selected row IDs; exit early if nothing is selected
        selected = self.tree.selection()

        if len(selected) == 1:
            self.resend_button.config(state="normal")
        else:
            self.resend_button.config(state="disabled")

        if not selected:
            return

        blocks = []

        # Extract column values for each selected row and format them
        for item_id in selected:
            values = self.tree.item(item_id, "values")

            # Build a readable message block for the preview panel
            message_text = (f"Sender: {values[3]} \t Date Sent: {values[0]} \t Received By: {values[4]} \n"
                        f"Subject: {values[1]} \n"
                        f"Message: {values[2]}")
            blocks.append(message_text)

        # Combine multiple selected messages into one display string
        final_text = "\n\n".join(blocks)

        # Update the message preview text box
        self.mess_display.config(state="normal")
        self.mess_display.delete("1.0", tk.END)
        self.mess_display.insert(tk.END, final_text)
        self.mess_display.config(state="disabled")

    def search(self) -> None:
        """
        Search the database for records
        """
        # Build datetime boundaries using the selected start/end dates
        start = datetime.combine(self.startdate_entry.get_date(), time.min)
        end = datetime.combine(self.enddate_entry.get_date(), time.max)
        keyword = self.keyword_variable.get()

        # Prevent invalid date ranges from being submitted
        if start > end:
            messagebox.showerror("Invalid Date Range", "End date must be after start date")
            return

        # Clear any previous results and message preview
        self.clear()

        # Query the database through the repository layer
        try:
            all_data = self.repo.search(start, end, keyword)
        except Exception:
            messagebox.showerror("Internal Error", "This feature cannot run on your "
                                                   "computer due to a missing or incompatible driver.")
            return

        # Show a message if no results were found
        if not all_data:
            messagebox.showinfo(
                "Search Results",
                "No notifications matched your search criteria."
            )

        # Insert each record into the Treeview
        for data in all_data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    self.format_dt(data.get_date()),
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

        # Reset filters and clear the UI before loading all records
        self.clear()

        # Retrieve all records from the repository
        try:
            all_data = self.repo.display_all()
        except Exception:
            messagebox.showerror(
                "Internal Error",
                "This feature cannot run due to a missing or incompatible database driver"
            )
            return

        # Populate the Treeview with all available records
        for data in all_data:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    self.format_dt(data.get_date()),
                    data.get_subject(),
                    data.get_message(),
                    data.get_sender(),
                    data.get_recipients()
                )
            )

    def clear_message_display(self) -> None:
        """
        Helper function to clear message display
        """
        self.mess_display.config(state="normal")
        self.mess_display.delete("1.0", tk.END)
        self.mess_display.config(state="disabled")

    def format_dt(self, dt: datetime | str) -> str:
        """
        Convert a datetime or ISO-formatted string into a consistent
        mm-dd-yyyy HH:MM:SS display format. If parsing fails, return
        the original value unchanged.
        """
        if isinstance(dt, datetime):
            return dt.strftime("%m-%d-%Y %H:%M:%S")
        try:
            parsed = datetime.fromisoformat(dt)
            return parsed.strftime("%m-%d-%Y %H:%M:%S")
        except Exception:
            return dt

    def sort_column(self, column: str, reverse: bool) -> None:
        """
        Sorts the Treeview rows by the given column.
        Sorting is case-insensitive for strings.
        Updates column headers with sort indicators.
        """

        # Extract (value, row_id) pairs for sorting
        items = [(self.tree.set(k, column), k) for k in self.tree.get_children("")]

        # Sort values, normalizing strings to lowercase for consistent ordering
        items.sort(
            key=lambda t: t[0].lower() if isinstance(t[0], str) else t[0],
            reverse=reverse)

        # Reorder rows in the Treeview based on the sorted order
        for index, (_, row_id) in enumerate(items):
            self.tree.move(row_id, "", index)

        # Update the clicked column header with a sort arrow
        arrow = " ▲" if not reverse else " ▼"
        title = self.columns[column][0]
        self.tree.heading(column, text=title + arrow, command=lambda: self.sort_column(column, not reverse))

        # Reset all other column headers to their default state
        for other_column in self.columns:
            if other_column != column:
                title = self.columns[other_column][0]
                self.tree.heading(
                    other_column,
                    text=title,
                    command=lambda c=other_column: self.sort_column(c, False))
        self.tree.heading(column, command=lambda: self.sort_column(column, not reverse))

    def reset_sort_indicators(self):
        """
        Restore all column headers to their default text and remove
        any sort arrows or active sort state
        """
        for col, (title, _) in self.columns.items():
            self.tree.heading(col,
                              text=title,
                              command=lambda c=col: self.sort_column(c, False))

    def export_csv(self) -> None:
        """
        Export the notification log records currently displayed in the
        Treeview to a CSV file selected by the user.

        If the user cancels the save dialog, no file is created.
        """

        rows = self.tree.get_children()

        if not rows:
            messagebox.showwarning(
                "No Records",
                "There are no notification log records to export."
            )
            return

        # Prompt the user to select a save location and filename
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )

        # Exit if the user cancels the save operation
        if not filename:
            return

        # Create the CSV file and write column headers
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Date",
                    "Subject",
                    "Message",
                    "Sender",
                    "Recipients",
                ])

                # Export each row currently displayed in the Treeview
                for item_id in self.tree.get_children():
                    writer.writerow(self.tree.item(item_id, "values"))

            messagebox.showinfo(
                "Export Complete",
                "Notification log exported successfully.")

        except Exception:
            messagebox.showerror(
                "Export Failed",
                "Unable to save the selected file."
            )
