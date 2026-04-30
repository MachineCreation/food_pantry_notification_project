#!/usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: t_database.py
# Author: Justin Crump
# 2026-04-29
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: database class for basic database functions

# Local imports
from env import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

# Python imports
import pyodbc

class Database:
    """
    Provides database connectivity for the application.

    This class is responsible for:
    - Verifying that the required ODBC driver is installed.
    - Creating and returning new database connection.
    """
    REQUIRED_DRIVER = "ODBC Driver 17 for SQL Server"

    @classmethod
    def check_driver(cls) -> None:
        """
        Ensure that the required ODBC driver is installed.

        Raises:
            RuntimeError: If the required ODBC driver is not installed.
        """
        installed = pyodbc.drivers()

        # Check if the required driver is present
        if cls.REQUIRED_DRIVER not in installed:
            installed_list = ", ".join(installed) or "None"
            raise RuntimeError(
                f"Required ODBC driver '{cls.REQUIRED_DRIVER}' not installed.\n"
                f"Installed: {installed_list}"
            )

    @classmethod
    def connect(cls) -> pyodbc.Connection:
        """
        Create and return a new database connection

        Returns:
            pyodbc.Connection: A new connection to the SQL Server database.

            Raises:
                RunTimeError: If the required ODBC driver is missing
                pyodbc.Error: If the connection attempt fails.
        """
        # Ensure the driver exists before attempting to connect
        cls.check_driver()

        # Build the connection string
        conn_str = (
            f"DRIVER={{{cls.REQUIRED_DRIVER}}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
        )

        #Return a new connection object
        return pyodbc.connect(conn_str)
