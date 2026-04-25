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


class FoodPantryProject():
    '''
    main GUI logic for app
    '''
    __gui: GUI | None = None

    def __init__(self):
        self.__gui = GUI()

    def run(self):
        '''
        run the app
        '''
        try:
            if self.__gui:
                self.__gui.run_gui()
            else:
                raise ValueError("No GUI found in instance")
        except ValueError as e:
            print(f'{e}')


if __name__ == "__main__":
    app = FoodPantryProject()
    app.run()
