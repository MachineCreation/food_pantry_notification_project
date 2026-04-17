#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: Database.py
# Author: Joseph Egan
# 2026-04-17
# Sources: 
# Contributors: 
# -------------------------------------------------------------------------------
# Description: database class for basic database functions

# Local imports

# python imports
import sqlite3

class Database():
    '''
    class for creating sqlite3 database connection and cursor.
    creating, altering, and querying sqlite3 databases.
    Provides methods to connect to a sqlite3 database, execute queries, and manage transactions.
    '''

    __connection: sqlite3.Connection | None = None
    __cursor: sqlite3.Cursor | None = None


    def __init__(self):
        pass

    def connect(self):
        '''
        Establishes a connection to the sqlite3 database and creates a cursor for executing SQL statements.
        :param self: instance of the Database class
        '''
        try:
            self.__connection = sqlite3.connect("database.db")
            self.make_cursor()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to connect to database: {e}")

    def disconnect(self):
        '''
        Closes the connection to the sqlite3 database and the associated cursor.
        :param self: instance of the Database class
        '''
        try:
            if self.__cursor:
                self.__cursor.close()
                self.__cursor = None
            if self.__connection:
                self.__connection.close()
                self.__connection = None
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to disconnect from database: {e}")

    def make_cursor(self):
        '''
        Creates a new cursor object for executing SQL statements.
        :param self: instance of the Database class
        '''
        try:
            if self.__connection:
                self.__cursor = self.__connection.cursor()
            else:
                raise ConnectionError("Database connection is not established.")
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to create cursor: {e}")