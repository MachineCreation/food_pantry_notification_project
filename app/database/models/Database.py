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

            result = None

            # cursor.description is not None when the query returned columns.
            # This works for SELECT and INSERT ... OUTPUT.
            if self.__cursor.description is not None:
                if fetch_all:
                    result = self.__cursor.fetchall()
                else:
                    result = self.__cursor.fetchone()

            self.__connection.commit()
            return result

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
            uid = self.execute_query(
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

                OUTPUT INSERTED.user_id

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

            self.get_new_user_notes(uid)
            self.set_user_settings(uid)
            return True

        except pymssql.Error as e:
            print(f'an error occurred: {e}')
            return False

    # --------------------
    def get_new_user_notes(
            self,
            user_id: int
    ) -> None:
        '''

        '''
        self.ensure_connection()

        get_notes_query = \
            '''
            INSERT INTO user_dashboard_notifications (user_id, notification_id)
            SELECT %s, notification_id
            FROM NOTIFICATIONS
            WHERE date_time BETWEEN DATEADD(DAY, -7, GETDATE()) AND GETDATE();
            '''

        try:
            self.execute_query(
                get_notes_query,
                (user_id,)
            )

        except pymssql.Error as e:
            print(f'SQL Error on database.get_notes: {e.with_traceback(None)}')

    # --------------------
    def update_last_login(
            self,
            user_id: int,
            date: datetime
    ) -> bool:
        '''
        update last login attribute in user_settings by user_id
        '''

        update_last_login_query = \
            '''
            UPDATE user_settings
            SET last_login = %s
            WHERE user_id = %s;
            '''

        try:
            self.execute_query(
                update_last_login_query,
                (
                    date,
                    user_id
                )
            )

            return True

        except pymssql.Error as e:
            print(f'{e.with_traceback}')
            print('Error from database.update_last_login')
            return False

    # --------------------
    def set_user_settings(
            self,
            user_id,
            notification_type: str | None = "email"
    ) -> None:
        '''

        '''

        user_settings_query = \
            '''
            INSERT INTO user_settings (user_id, notification_type)

            VALUES(%s, %s)

            '''

        try:
            self.execute_query(
                user_settings_query,
                (user_id, notification_type)
            )

        except pymssql.Error as e:
            print('Error on database.set_user_settings: '
                  f'{e.with_traceback(None)}')

    # --------------------
    def get_user_settings(
        self,
        user_id: int
    ) -> Tuple[bool, dict | None]:
        """
        Get user settings and dashboard notifications for a user.

        Dashboard notifications are stored in the user_dashboard_notifications
        table. Each notification returned includes an is_new value based on
        whether the notification was created after the user's last_login.

        :param user_id: int user id to get settings for
        :return: tuple of (success, settings dict or None)
        """

        from app.logic.models.Notification import Notification
        self.ensure_connection()

        get_user_settings_query = """
        SELECT
            us.notification_type,
            us.last_login,

            n.notification_id,
            n.sender_id,
            n.template_id,
            n.subject,
            n.body_text,
            n.num_recip,
            n.image_id,
            n.date_time,

            CASE
                WHEN us.last_login IS NULL THEN 0
                WHEN n.date_time > us.last_login THEN 1
                ELSE 0
            END AS is_new

        FROM user_settings us

        LEFT JOIN user_dashboard_notifications udn
            ON udn.user_id = us.user_id

        LEFT JOIN NOTIFICATIONS n
            ON n.notification_id = udn.notification_id

        WHERE us.user_id = %s

        ORDER BY
            n.date_time DESC
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
                "last_login": result[0][1],
                "dashboard_notifications": []
            }

            for row in result:
                notification_id = row[2]

                # This happens if the user has settings,
                # but no dashboard notifications assigned yet.
                if notification_id is None:
                    continue

                notification = Notification(
                    sender_id=row[3],
                    template_id=row[4],
                    subject=row[5],
                    message=row[6],
                    image_id=row[8],
                )
                notification.notification_id = notification_id
                notification.date = row[9]
                notification.num_recipients = row[7]
                notification.is_new = bool(row[10])

                settings["dashboard_notifications"].append(notification)

            return True, settings

        except pymssql.Error as error:
            print(f"Error getting user settings: {error}")
            return False, None

    # --------------------
    def add_phone_number(
            self,
            user_id: int,
            phone_number: str
    ) -> bool:
        '''
        add a phone number to the user's account for sms notifications
        :param user_id: int user id to add phone number for
        :param phone_number: str phone number to add
        :return: bool indicating success or failure of the operation
        '''

        add_phone_number_query = '''
        UPDATE user_settings
        SET phone_number = %s
        WHERE user_id = %s;
        '''

        try:
            self.execute_query(
                add_phone_number_query,
                (phone_number, user_id),
                fetch_all=False
            )
            return True

        except pymssql.Error as error:
            print(f"Error adding phone number: {error}")
            return False

    # --------------------
    def update_user_notification_type(
            self,
            user_id: int,
            notification_type: str
    ) -> bool:
        '''
        update the user's notification type
        :param user_id: int user id to update
        :param notification_type: str notification type to set
        :return: bool indicating success or failure of the operation
        '''

        update_notification_type_query = '''
        UPDATE user_settings
        SET notification_type = %s
        WHERE user_id = %s;
        '''

        try:
            self.execute_query(
                update_notification_type_query,
                (notification_type, user_id),
                fetch_all=False
            )
            return True

        except pymssql.Error as error:
            print(f"Error updating notification type: {error}")
            return False

    # --------------------
    def remove_user_dashboard_notifications(
            self,
            user_id: int,
            notification_ids: set[int]
    ) -> bool:
        '''
        Remove specified notifications from the user's dashboard notifications.
        :param user_id: int user id to remove notifications for
        :param notification_ids: set of int notification ids to remove
        :return: bool indicating success or failure of the operation
        '''
        if not notification_ids:
            print("No notification IDs provided for removal.")
            return False

        placeholders = ', '.join(['%s'] * len(notification_ids))
        delete_query = f'''
            DELETE FROM user_dashboard_notifications
            WHERE user_id = %s AND notification_id IN ({placeholders});
        '''

        try:
            self.execute_query(
                delete_query,
                (user_id, *notification_ids),
                fetch_all=False
            )
            return True

        except pymssql.Error as error:
            print(f"Error removing dashboard notifications: {error}")
            return False

    # --------------------
    def lock_account(
            self,
            user_id: int
    ) -> bool:
        '''
        lock the user's account by setting their role to 4
        :param user_id: int user id to lock
        :return: bool indicating success or failure of the operation
        '''

        lock_account_query = '''
        UPDATE USERS
        SET role_id = 4
        WHERE user_id = %s;
        '''

        try:
            self.execute_query(
                lock_account_query,
                (user_id,),
                fetch_all=False
            )
            return True

        except pymssql.Error as error:
            print(f"Error locking account: {error}")
            return False

# ------------------------ notification log methods ---------------------------
    def get_recipients(self) -> List[Tuple[str, str, str]]:
        '''
        gets a list of subscriber emails from the database and passes it
            forward
        '''
        get_recipients_query = '''
        SELECT u.email_address, us.phone_number, us.notification_type
        FROM USERS u
        JOIN user_settings us ON u.user_id = us.user_id
        WHERE u.role_id IN (0, 1, 3);
        '''

        try:
            recipients = list(
                self.execute_query(
                    get_recipients_query,
                    fetch_all=True
                )
            )
            print(recipients)
            return recipients
        except ValueError or pymssql.Error:
            print('no recipients returned from database.get_recipients')

    # --------------------
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
        SET NOCOUNT ON;
        INSERT INTO NOTIFICATIONS (
                sender_id,
                template_id,
                subject,
                body_text,
                num_recip,
                image_id,
                date_time
        )
        OUTPUT INSERTED.notification_id
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        '''

        add_notification_to_all_users_query = '''
        INSERT INTO user_dashboard_notifications (user_id, notification_id)
        SELECT user_id, %s
        FROM USERS;
        '''

        try:
            # log the notification and return generated id
            print('logging notification')
            notification_id = self.execute_query(
                log_notification_query,
                fetch_all=False,
                parameters=(
                    sender_id,
                    template_id,
                    subject,
                    message,
                    num_recipients,
                    image_id,
                    date
                )
            )

            print(f'notification logged with id: {notification_id}')

            if notification_id is None:
                print('Failed to log notification: No ID returned')
                raise pymssql.Error()

            # add associated notification to all users
            print('associating notification with users')
            self.execute_query(
                add_notification_to_all_users_query,
                (notification_id[0],),
                fetch_all=False
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
