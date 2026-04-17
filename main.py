#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename:main.py
# Author: Joseph Egan
# 2026-04-17
# Sources: None
# Contributors: 
# -------------------------------------------------------------------------------
# Description: Main root app file for initiating instance

# Local imports
from app.GUI.GUI import GUI

# python imports
from tkinter import Tk

def main():

    # create the main tkinter root window
    root = Tk()
    root.title("Food Pantry Notification App")

    gui = GUI(root)

    root.mainloop()

if __name__ == "__main__":
    main()
