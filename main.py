#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:main.py
# Author: Lloyd Truong
# 2026-04-23
# Sources: None
# Contributors: 
# -------------------------------------------------------------------------------
# Description: Main root app file for initiating instance

# Local imports
from app.GUI.GUI import GUI

# python imports
from tkinter import Tk
from app.Database.models.Database import Database


def main():

    # create the main tkinter root window
    root = Tk()
    root.title("Food Pantry Notification App")

    db = Database()
    db.connect()

    app_context = {"database": db}

    # create the GUI instance
    gui = GUI(root, app_context)

    # start the main event loop
    root.mainloop()

    db.disconnect()


if __name__ == "__main__":
    main()

