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
import env

# python imports
import sqlite3

class Database():
    '''
    class for creating sqlite3 database connection and cursor.
    creating, altering, and querying sqlite3 databases.
    Provides methods to connect to a sqlite3 database, execute queries, and manage transactions.
    '''

    # database url from env.py should be from .env but this is for simplicity
    database_url: str | None = env.DATABASE_URL

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
            self.__connection = sqlite3.connect(self.database_url)
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
        
    def execute_query(self, query: str, parameters: tuple = (), fetch_all: bool = True):
        '''
        Executes a SQL query using the database cursor.
        :param self: instance of the Database class
        :param query: SQL query string to execute
        :param parameters: optional tuple of parameters to pass to the query
        :param fetch_all: if True, fetch all results from the query and return them, 
        otherwise return one.
        :return: result of the query, either all rows (list of tuples) if fetch_all is True, 
        or a single row (tuple) if fetch_all is False
        '''
        if not self.__cursor:
            raise ConnectionError("Database cursor is not established.")
        try:
            if parameters:
                self.__cursor.execute(query, parameters)
            else:
                self.__cursor.execute(query)
            self.__connection.commit()
            if fetch_all:
                return self.__cursor.fetchall()
            else:
                return self.__cursor.fetchone()
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to execute query: {e}")

    # --------------------
    def drop_table(self, table_name: str):
        '''
        drops a table from the database if it exists
        :param self: instance of the Database class
        :param table_name: name of the table to drop
        '''
        if not self.__cursor:
            raise ConnectionError("Database cursor is not established.")
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        try:
            self.__cursor.execute(drop_table_query)
            self.__connection.commit()
            print(f"Table {table_name} dropped successfully.")
        except sqlite3.Error as e:
            raise sqlite3.Error(f"Failed to drop table {table_name}: {e}")
        
    # --------------------
    @staticmethod
    def rebuild_database():
        '''
        runs database rebuild script located in app/Database/setup/create_database.py
        '''
        from app.Database.setup.create_database import main
        print("Rebuilding database...")
        main()