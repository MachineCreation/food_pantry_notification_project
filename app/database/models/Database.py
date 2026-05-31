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
import pymssql
import bcrypt
from typing import Tuple, List
from datetime import datetime
from itertools import chain


class Database:
    '''
    Handles SQL Server database connection, query execution,
    authentication, and user signup.
    '''

    __database: str = env.DATABASE_URL
    __db_name: str = env.DB_NAME
    __db_username: str = env.DB_USERNAME
    __db_password: str = env.DB_PASSWORD

    def __init__(self):

        self.__connection: pymssql.Connection | None = None
        self.__cursor: pymssql.Cursor | None = None

        self.connect()

    # -------------------- connection methods --------------------

    def connect(self) -> None:
        '''
        Establish database connection and cursor.
        '''
        try:
            self.__connection = pymssql.connect(
                server=self.__database,
                user=self.__db_username,
                password=self.__db_password,
                database=self.__db_name,
                timeout=30
            )
            self.__cursor = self.__connection.cursor()

        except pymssql.Error as error:
            raise ConnectionError(f"Failed to connect to database: {error}")

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

        except pymssql.Error as error:
            raise pymssql.Error(f"Failed to disconnect from database: {error}")

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

        if self.__cursor is None:
            raise ConnectionError("Database cursor is not available.")

        if self.__connection is None:
            raise ConnectionError("Database connection is not available.")

        try:
            self.__cursor.execute(query, parameters)

            query_starts_with = query.strip().lower()

            if query_starts_with.startswith("select"):
                if fetch_all:
                    return self.__cursor.fetchall()

                return self.__cursor.fetchone()

            self.__connection.commit()
            return None

        except pymssql.Error as error:
            self.__connection.rollback()
            raise pymssql.Error(f"Failed to execute query: {error}") from error

    # -------------------- user methods --------------------

    def authenticate_user(
            self,
            user: str,
            password: str,
            id_type: str
            ) -> tuple[bool, str | None, str | None]:
        '''
        Authenticate user by username or email.

        :return: (authenticated, role, username)
        '''
        if id_type not in ("username", "email"):
            print('missing parameters')
            return False, None, None, None

        column_name = "username" if id_type == "username" else "email_address"

        query = f'''
            SELECT password_hash, role_id, username, user_id
            FROM USERS
            WHERE {column_name} = %s;
        '''

        try:
            result = self.execute_query(
                query,
                (user,),
                fetch_all=False
            )

            if not result:
                return False, None, None, None

            stored_password, user_role, username, user_id = result

            authenticated = bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            )

            return authenticated, user_role, username, user_id

        except pymssql.Error as e:
            print(f'SQL error: {e}')
            return False, None, None, None

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
                WHERE username = %s OR email_address = %s;
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
            self.execute_query(
                '''
                INSERT INTO USERS (
                    first_name,
                    last_name,
                    username,
                    email_address,
                    password_hash,
                    allergies,
                    campus,
                    role_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                ''',
                (
                    first_name,
                    last_name,
                    username,
                    email,
                    hashed_password,
                    allergies,
                    campus,
                    role
                ),
                fetch_all=False
            )
            return True

        except pymssql.Error as e:
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

        except pymssql.Error as e:
            print(f'SQL Error: {e}')
            return False, ('none', 'none')
        
    # --------------------
    def get_user_settings(
            self,
            user_id: int
            ) -> Tuple[bool, dict | None]:
        """
        Get user settings and dashboard notifications for a user.

        dashboard_view is stored as a comma-separated list of notification_ids.
        The returned settings dict includes dashboard_notifications as a list
        of notification objects/dicts.

        :param user_id: int user id to get settings for
        :return: (success, settings dict or None)
        """

        self.ensure_connection()

        get_user_settings_query = """
        SELECT
            us.notification_type,
            us.dashboard_view,
            us.last_login,

            n.notification_id,
            n.sender_id,
            n.template_id,
            n.subject,
            n.body_text,
            n.num_recip,
            n.image_id,
            n.date_time
        FROM user_settings us
        CROSS APPLY STRING_SPLIT(us.dashboard_view, ',') s
        LEFT JOIN NOTIFICATIONS n
            ON n.notification_id = TRY_CAST(TRIM(s.value) AS INT)
        WHERE us.user_id = %s
        """

        try:
            result = self.execute_query(
                get_user_settings_query,
                (user_id,),
                fetch_all=True
            )

            if not result:
                return False, None

            settings = {
                "notification_type": result[0][0],
                "dashboard_view": (
                    [note.strip() for note in result[0][1].split(",")]
                    if result[0][1]
                    else []
                ),
                "last_login": result[0][2],
                "dashboard_notifications": []
            }

            for row in result:
                notification_id = row[3]

                # This happens when dashboard_view is NULL/empty
                # or contains an invalid notification_id.
                if notification_id is None:
                    continue

                notification = {
                    "notification_id": row[3],
                    "sender_id": row[4],
                    "template_id": row[5],
                    "subject": row[6],
                    "body_text": row[7],
                    "num_recip": row[8],
                    "image_id": row[9],
                    "date_time": row[10]
                }

                settings["dashboard_notifications"].append(notification)

            return True, settings

        except Exception as e:
            print(f"Error getting user settings: {e}")
            return False, None


# ------------------------ notification log methods ---------------------------
    def get_recipients(self) -> List[str]:
        '''
        gets a list of subscriber emails from the database and passes it
            forward
        '''
        get_recipients_query = '''
        SELECT email_address
        FROM USERS
        WHERE role_id = 1
        '''

        try:
            recipients = list(chain.from_iterable(
                    self.execute_query(
                        get_recipients_query,
                        fetch_all=True
                    )
                )
            )
            return recipients
        except ValueError or pymssql.Error:
            print('no recipients returned from database.get_recipients')

    def log_notification(
            self,
            date: datetime,
            subject: str,
            message: str,
            sender_id: int,
            num_recipients: int,
            image_id: int | None = None,
            template_id: int | None = None,
    ) -> bool:
        '''
        log the notification in the database
        :param date: datetime of the notification
        :param subject: string subject of the notification
        :param message: string message content of the notification
        :param user_id: int user id of the sender
        :param num_recipients: int number of recipients that received the
            notification
        :param template: string name of the template used for the notification
        :return: boolean indicating success or failure of the logging operation
        '''

        self.ensure_connection()

        log_notification_query = '''
        INSERT INTO NOTIFICATIONS (
                sender_id,
                template_id,
                subject,
                body_text,
                num_recip,
                image_id,
                date_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''

        try:
            print('logging notification')
            self.execute_query(
                log_notification_query,
                (
                    sender_id,
                    template_id,
                    subject,
                    message,
                    num_recipients,
                    image_id,
                    date
                )
            )

        except pymssql.Error:
            print('Error logging notification in database.log_notification')

# ---------------------------- template methods ------------------------------
    def get_all_templates(self) -> List[Tuple]:
        '''
        get all templates from the database and return them to the caller
        :return: list of table row tuples. Tuple attribute order
            template_id: int,
            template_name: str,
            creator_id: int,
            subject: str,
            template_body: str,
            tags: List
        '''

        get_all_templates_query = '''
        SELECT *
        FROM TEMPLATE
        '''

        try:
            templates = self.execute_query(
                get_all_templates_query
            )

            return templates

        except pymssql.Error as e:
            print(f'Error on database.get_all_templates\n{e.with_traceback}')

# --------------------------------- static -----------------------------------
    @staticmethod
    def rebuild_database():
        '''
        runs database rebuild script located in
        app/database/setup/create_database.py
        '''
        pass
