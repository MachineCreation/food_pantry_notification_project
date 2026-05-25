# -------------------------------------------------------------------------------
# filename: app/tests/test_database.py
# Author: Joseph Egan
# 2026-05-04
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: unittest suite for database methods

import unittest

import bcrypt
import pymssql

from app.database.models.Database import Database


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.database = Database()
        except Exception as error:
            raise unittest.SkipTest(
                f"Database not available for tests: {error}"
            ) from error

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_database_tests()
        cls.database.disconnect()

    def setUp(self):
        self.setup_database_tests()

    def tearDown(self):
        self.cleanup_database_tests()

    @classmethod
    def setup_database_tests(cls):
        """
        Creates predictable test users.
        Run this before database tests.
        """
        cls.database.execute_query(
            """
            DELETE FROM USERS
            WHERE username LIKE %s
               OR email_address LIKE %s;
            """,
            ("test_%", "test_%@example.com"),
            fetch_all=False,
        )

        password_hash = bcrypt.hashpw(
            "CorrectPassword123".encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

        cls.database.execute_query(
            """
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
            """,
            (
                "Test",
                "User",
                "test_existing_user",
                "test_existing_user@example.com",
                password_hash,
                False,
                "Main",
                1,
            ),
            fetch_all=False,
        )

    @classmethod
    def cleanup_database_tests(cls):
        """
        Removes test users after database tests.
        """
        cls.database.execute_query(
            """
            DELETE FROM USERS
            WHERE username LIKE %s
               OR email_address LIKE %s;
            """,
            ("test_%", "test_%@example.com"),
            fetch_all=False,
        )

    # -------------------- ensure_connection --------------------

    def test_ensure_connection_with_existing_connection(self):
        self.assertIsNone(self.database.ensure_connection())

    def test_ensure_connection_after_disconnect(self):
        self.database.disconnect()
        self.assertIsNone(self.database.ensure_connection())

    def test_ensure_connection_when_private_connection_is_none(self):
        setattr(self.database, "_Database__connection", None)
        self.assertIsNone(self.database.ensure_connection())

    def test_ensure_connection_when_private_cursor_is_none(self):
        setattr(self.database, "_Database__cursor", None)
        self.assertIsNone(self.database.ensure_connection())

    def test_ensure_connection_repeated_call(self):
        self.assertIsNone(self.database.ensure_connection())
        self.assertIsNone(self.database.ensure_connection())

    # -------------------- execute_query --------------------

    def test_execute_query_select_all_users_returns_list(self):
        result = self.database.execute_query(
            "SELECT username FROM USERS WHERE username = %s;",
            ("test_existing_user",),
            fetch_all=True,
        )
        self.assertIsInstance(result, list)

    def test_execute_query_select_one_user_returns_row(self):
        result = self.database.execute_query(
            "SELECT username FROM USERS WHERE username = %s;",
            ("test_existing_user",),
            fetch_all=False,
        )
        self.assertIsNotNone(result)

    def test_execute_query_select_missing_user_returns_none(self):
        result = self.database.execute_query(
            "SELECT username FROM USERS WHERE username = %s;",
            ("test_missing_user",),
            fetch_all=False,
        )
        self.assertIsNone(result)

    def test_execute_query_insert_query_returns_none(self):
        password_hash = bcrypt.hashpw(
            "Password123".encode("utf-8"),
            bcrypt.gensalt(12)
        ).decode("utf-8")

        result = self.database.execute_query(
            """
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
            """,
            (
                "Test",
                "Insert",
                "test_insert_user",
                "test_insert_user@example.com",
                password_hash,
                False,
                "Main",
                1,
            ),
            fetch_all=False,
        )

        self.assertIsNone(result)

    def test_execute_query_bad_query_raises_pymssql_error(self):
        with self.assertRaises(pymssql.Error):
            self.database.execute_query(
                "SELECT * FROM TABLE_THAT_DOES_NOT_EXIST;",
                (),
                fetch_all=True,
            )

    # -------------------- authenticate_user --------------------

    def test_authenticate_user_valid_username_and_password(self):
        authenticated, role_id, username, user_id = self.database.authenticate_user(
            user="test_existing_user",
            password="CorrectPassword123",
            id_type="username",
        )
        self.assertTrue(authenticated)
        self.assertEqual(role_id, 1)
        self.assertEqual(username, "test_existing_user")
        self.assertIsNotNone(user_id)

    def test_authenticate_user_valid_email_and_password(self):
        authenticated, role_id, username, user_id = self.database.authenticate_user(
            user="test_existing_user@example.com",
            password="CorrectPassword123",
            id_type="email",
        )
        self.assertTrue(authenticated)
        self.assertEqual(role_id, 1)
        self.assertEqual(username, "test_existing_user")
        self.assertIsNotNone(user_id)

    def test_authenticate_user_wrong_password(self):
        authenticated, role_id, username, user_id = self.database.authenticate_user(
            user="test_existing_user",
            password="WrongPassword123",
            id_type="username",
        )
        self.assertFalse(authenticated)
        self.assertEqual(role_id, 1)
        self.assertEqual(username, "test_existing_user")
        self.assertIsNotNone(user_id)

    def test_authenticate_user_missing_user(self):
        authenticated, role_id, username, user_id = self.database.authenticate_user(
            user="test_missing_user",
            password="CorrectPassword123",
            id_type="username",
        )
        self.assertEqual((authenticated, role_id, username, user_id), (False, None, None, None))

    def test_authenticate_user_bad_id_type(self):
        authenticated, role_id, username, user_id = self.database.authenticate_user(
            user="test_existing_user",
            password="CorrectPassword123",
            id_type="phone",
        )
        self.assertEqual((authenticated, role_id, username, user_id), (False, None, None, None))

    # -------------------- sign_up_user --------------------

    def test_sign_up_user_valid_new_user(self):
        result = self.database.sign_up_user(
            username="test_signup_valid",
            password="Password123",
            email="test_signup_valid@example.com",
            first_name="Test",
            last_name="Signup",
            allergies=False,
            campus="Main",
            role=1,
        )
        self.assertTrue(result)

    def test_sign_up_user_duplicate_username(self):
        result = self.database.sign_up_user(
            username="test_existing_user",
            password="Password123",
            email="test_duplicate_username@example.com",
            first_name="Test",
            last_name="Duplicate",
            allergies=False,
            campus="Main",
            role=1,
        )
        self.assertFalse(result)

    def test_sign_up_user_duplicate_email(self):
        result = self.database.sign_up_user(
            username="test_duplicate_email",
            password="Password123",
            email="test_existing_user@example.com",
            first_name="Test",
            last_name="Duplicate",
            allergies=False,
            campus="Main",
            role=1,
        )
        self.assertFalse(result)

    def test_sign_up_user_missing_username(self):
        result = self.database.sign_up_user(
            username="",
            password="Password123",
            email="test_missing_username@example.com",
            first_name="Test",
            last_name="Missing",
            allergies=False,
            campus="Main",
            role=1,
        )
        self.assertFalse(result)

    def test_sign_up_user_missing_password(self):
        result = self.database.sign_up_user(
            username="test_missing_password",
            password="",
            email="test_missing_password@example.com",
            first_name="Test",
            last_name="Missing",
            allergies=False,
            campus="Main",
            role=1,
        )
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
