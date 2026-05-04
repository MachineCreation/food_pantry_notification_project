#!/usr/bin/env python3.14

import env
import pyodbc


class Database:
    def __init__(self):
        self.host = env.DB_HOST
        self.user = env.DB_USER
        self.password = env.DB_PASS
        self.database = env.DB_NAME
        self._connection = None
        self._cursor = None

    def connect(self):
        """
        opens a connection to the SQL Server database
        """
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={self.host},1433;"
            f"DATABASE={self.database};"
            f"UID={self.user};"
            f"PWD={self.password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )
        self._connection = pyodbc.connect(connection_string, timeout=10)
        self._cursor = self._connection.cursor()
        print("Successfully connected to PCC Remote Database!")

    def disconnect(self):
        """
        closes the database cursor and connection if they are open
        """
        if self._cursor:
            self._cursor.close()
            self._cursor = None
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query: str, parameters: tuple = (), fetch_all: bool = True):
        """
        executes a SQL query using the active database cursor
        :param query: SQL query string to execute
        :param parameters: optional tuple of values for parameterized SQL
        :param fetch_all: if True, return all rows for SELECT queries otherwise return one row
        :return: query results for SELECT statements or True for successful non-SELECT statements
        """
        if not self._cursor:
            raise ConnectionError("Database cursor is not established.")

        if parameters:
            self._cursor.execute(query, parameters)
        else:
            self._cursor.execute(query)

        is_select = query.strip().upper().startswith("SELECT")
        if is_select:
            return self._cursor.fetchall() if fetch_all else self._cursor.fetchone()

        self._connection.commit()
        return True

    def drop_table(self, table_name: str):
        """
        drops the given table from the database if it exists
        :param table_name: name of the table to remove
        """
        if not self._cursor:
            raise ConnectionError("Database cursor is not established.")
        drop_table_query = f"DROP TABLE IF EXISTS {table_name};"
        try:
            self._cursor.execute(drop_table_query)
            self._connection.commit()
            print(f"Table {table_name} dropped successfully.")
        except pyodbc.Error as e:
            raise pyodbc.Error(f"Failed to drop table {table_name}: {e}")

    @staticmethod
    def rebuild_database():
        from app.Database.setup.create_database import main
        print("Rebuilding database...")
        main()
