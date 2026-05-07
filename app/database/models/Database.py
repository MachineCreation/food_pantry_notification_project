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

# Python imports
import pyodbc
import bcrypt
from typing import Tuple


class Database:
    '''
    Handles SQL Server database connection, query execution,
    authentication, and user signup.
    '''

    database: str | None = env.DATABASE_URL
    db_name: str = env.DB_NAME
    db_username: str = env.DB_USERNAME
    db_password: str = env.DB_PASSWORD

    def __init__(self):
        self.conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={self.database};"
            f"DATABASE={self.db_name};"
            f"UID={self.db_username};"
            f"PWD={self.db_password};"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;"
        )

        self.__connection: pyodbc.Connection | None = None
        self.__cursor: pyodbc.Cursor | None = None

        self.connect()

    # -------------------- connection methods --------------------

    def connect(self) -> None:
        '''
        Establish database connection and cursor.
        '''
        try:
            self.__connection = pyodbc.connect(self.conn_str)
            self.__cursor = self.__connection.cursor()

        except pyodbc.Error as error:
            raise pyodbc.Error(f"Failed to connect to database: {error}")

    def disconnect(self) -> None:
        '''
        Close cursor and database connection.
        '''
        try:
            if self.__cursor:
                self.__cursor.close()
                self.__cursor = None

            if self.__connection:
                self.__connection.close()
                self.__connection = None

        except pyodbc.Error as error:
            raise pyodbc.Error(f"Failed to disconnect from database: {error}")

    def ensure_connection(self) -> None:
        '''
        Reconnect if connection or cursor is missing.
        '''
        if self.__connection is None or self.__cursor is None:
            self.connect()

    # -------------------- query methods --------------------

    def execute_query(
            self,
            query: str,
            parameters: tuple = (),
            fetch_all: bool = True
            ) -> list[tuple] | tuple | None:
        '''
        Execute a SQL query.

        :param query: SQL query string
        :param parameters: optional query parameters
        :param fetch_all: True returns all rows, False returns one row
        :return: query results for SELECT, None for write queries
        '''
        self.ensure_connection()

        try:
            self.__cursor.execute(query, parameters)

            query_starts_with = query.strip().lower()

            if query_starts_with.startswith("select"):
                if fetch_all:
                    return self.__cursor.fetchall()
                return self.__cursor.fetchone()

            self.__connection.commit()
            return None

        except pyodbc.Error as error:
            if self.__connection:
                self.__connection.rollback()
            raise pyodbc.Error(f"Failed to execute query: {error}")

    def drop_table(self, table_name: str) -> None:
        '''
        Drop a table if it exists.
        '''
        if not table_name.isidentifier():
            raise ValueError("Invalid table name.")

        query = f"DROP TABLE IF EXISTS {table_name};"
        self.execute_query(query, fetch_all=False)

    # -------------------- user methods --------------------

    def authenticate_user(
            self,
            user_id: str,
            password: str,
            id_type: str
            ) -> tuple[bool, str | None, str | None]:
        '''
        Authenticate user by username or email.

        :return: (authenticated, role, username)
        '''
        if id_type not in ("username", "email"):
            print('missing parameters')
            return False, None, None

        column_name = "username" if id_type == "username" else "email_address"

        query = f'''
            SELECT password_hash, role_id, username
            FROM USERS
            WHERE {column_name} = ?;
        '''

        try:
            result = self.execute_query(
                query,
                (user_id,),
                fetch_all=False
            )

            if not result:
                return False, None, None

            stored_password, user_role, username = result

            authenticated = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            )

            return authenticated, user_role, username

        except pyodbc.Error as e:
            print(f'SQL error: {e}')
            return False, None, None

    # --------------------
    def sign_up_user(
            self,
            username: str,
            password: str,
            email: str,
            first_name: str,
            last_name: str,
            allergies: bool,
            campus: str,
            role: int = 1
            ) -> bool:
        '''
        Sign up a new user.
        '''
        required_fields = [
            username,
            password,
            email,
            first_name,
            last_name,
            campus
        ]

        if not all(required_fields):
            print("Not all fields provided")
            return False

        try:
            existing_user = self.execute_query(
                '''
                SELECT username, email_address
                FROM USERS
                WHERE username = ? OR email_address = ?;
                ''',
                (username, email),
                fetch_all=False
            )


            if existing_user:
                print(f'{username} already exists')
                return False


            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt(12)
            ).decode("utf-8")

            print('inserting user')
            did_create = self.execute_query(
                '''
                INSERT INTO USERS (
                    first_name,
                    last_name,
                    username,
                    email_address,
                    password_hash,
                    role_id
                )
                VALUES (?, ?, ?, ?, ?, ?);
                ''',
                (
                    first_name,
                    last_name,
                    username,
                    email,
                    hashed_password,
                    role
                ),
                fetch_all=False
            )
            return True

        except pyodbc.Error as e:
            print(f'an error occured: {e}')
            return False
        
    # --------------------
    def get_notes(self) -> Tuple[bool, Tuple[str]]:
        '''
        
        '''
        self.ensure_connection()

        get_notes_query = \
            '''
            SELECT TOP 5 date_time, subject, body_text
            FROM NOTIFICATIONS
            ORDER BY notification_id DESC;
            '''

        try:
            result = self.execute_query(
                get_notes_query,
                fetch_all=True
            )
            return True, result

        except pyodbc.Error as e:
            print(f'SQL Error: {e}')
            return False, ('none', 'none')

# --------------------------------- static ---------------------------------
    @staticmethod
    def rebuild_database():
        '''
        runs database rebuild script located in
        app/database/setup/create_database.py
        '''
        pass
