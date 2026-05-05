# -------------------------------------------------------------------------------
# filename: app/tests/test_database.py
# Author: Joseph Egan
# 2026-05-04
# Sources: 
# Contributors: 
# -------------------------------------------------------------------------------
# Description:A testing suite for units in database 

# Local imports
from app.database.models.Database import Database

# python imports
# app/tests/test_database.py

import pyodbc
import bcrypt


def setup_database_tests(database: Database):
    """
    Creates predictable test users.
    Run this before database tests.
    """

    database.execute_query("""
        DELETE FROM USERS
        WHERE username LIKE 'test_%'
           OR email_address LIKE 'test_%@example.com';
    """, fetch_all=False)

    password_hash = bcrypt.hashpw(
        "CorrectPassword123".encode("utf-8"),
        bcrypt.gensalt(12)
    ).decode("utf-8")

    database.execute_query("""
        INSERT INTO USERS (
            first_name,
            last_name,
            username,
            email_address,
            password_hash,
            role_id
        )
        VALUES (?, ?, ?, ?, ?, ?);
    """, (
        "Test",
        "User",
        "test_existing_user",
        "test_existing_user@example.com",
        password_hash,
        1
    ), fetch_all=False)


def cleanup_database_tests(database):
    """
    Removes test users after database tests.
    """

    database.execute_query("""
        DELETE FROM USERS
        WHERE username LIKE 'test_%'
           OR email_address LIKE 'test_%@example.com';
    """, fetch_all=False)


# -------------------- ensure_connection --------------------

def test_ensure_connection():
    return {
        "ensure connection with existing connection": {
            "params": {},
            "expected results": None
        },

        "ensure connection after disconnect": {
            "before": lambda db: db.disconnect(),
            "params": {},
            "expected results": None
        },

        "ensure connection when private connection is None": {
            "before": lambda db: setattr(db, "_Database__connection", None),
            "params": {},
            "expected results": None
        },

        "ensure connection when private cursor is None": {
            "before": lambda db: setattr(db, "_Database__cursor", None),
            "params": {},
            "expected results": None
        },

        "ensure connection repeated call": {
            "params": {},
            "expected results": None
        },
    }


# -------------------- execute_query --------------------

def test_execute_query():
    return {
        "select all users returns list": {
            "params": {
                "query": "SELECT username FROM USERS WHERE username = ?;",
                "parameters": ("test_existing_user",),
                "fetch_all": True
            },
            "expected type": list
        },

        "select one user returns row": {
            "params": {
                "query": "SELECT username FROM USERS WHERE username = ?;",
                "parameters": ("test_existing_user",),
                "fetch_all": False
            },
            "validate": lambda result: result is not None
        },

        "select missing user returns none": {
            "params": {
                "query": "SELECT username FROM USERS WHERE username = ?;",
                "parameters": ("test_missing_user",),
                "fetch_all": False
            },
            "expected results": None
        },

        "insert query returns none": {
            "params": {
                "query": """
                    INSERT INTO USERS (
                        first_name,
                        last_name,
                        username,
                        email_address,
                        password_hash,
                        role_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?);
                """,
                "parameters": (
                    "Test",
                    "Insert",
                    "test_insert_user",
                    "test_insert_user@example.com",
                    bcrypt.hashpw(
                        "Password123".encode("utf-8"),
                        bcrypt.gensalt(12)
                    ).decode("utf-8"),
                    1
                ),
                "fetch_all": False
            },
            "expected results": None
        },

        "bad query raises pyodbc error": {
            "params": {
                "query": "SELECT * FROM TABLE_THAT_DOES_NOT_EXIST;",
                "parameters": (),
                "fetch_all": True
            },
            "expected exception": pyodbc.Error
        },
    }


# -------------------- authenticate_user --------------------

def test_authenticate_user():
    return {
        "authenticate valid username and password": {
            "params": {
                "user_id": "test_existing_user",
                "password": "CorrectPassword123",
                "id_type": "username"
            },
            "expected results": (True, 1, "test_existing_user")
        },

        "authenticate valid email and password": {
            "params": {
                "user_id": "test_existing_user@example.com",
                "password": "CorrectPassword123",
                "id_type": "email"
            },
            "expected results": (True, 1, "test_existing_user")
        },

        "fail authentication with wrong password": {
            "params": {
                "user_id": "test_existing_user",
                "password": "WrongPassword123",
                "id_type": "username"
            },
            "expected results": (False, 1, "test_existing_user")
        },

        "fail authentication with missing user": {
            "params": {
                "user_id": "test_missing_user",
                "password": "CorrectPassword123",
                "id_type": "username"
            },
            "expected results": (False, None, None)
        },

        "fail authentication with bad id type": {
            "params": {
                "user_id": "test_existing_user",
                "password": "CorrectPassword123",
                "id_type": "phone"
            },
            "expected results": (False, None, None)
        },
    }


# -------------------- sign_up_user --------------------

def test_sign_up_user():
    return {
        "sign up valid new user": {
            "params": {
                "username": "test_signup_valid",
                "password": "Password123",
                "email": "test_signup_valid@example.com",
                "first_name": "Test",
                "last_name": "Signup",
                "allergies": False,
                "campus": "Main",
                "role": 1
            },
            "expected results": True
        },

        "fail signup duplicate username": {
            "params": {
                "username": "test_existing_user",
                "password": "Password123",
                "email": "test_duplicate_username@example.com",
                "first_name": "Test",
                "last_name": "Duplicate",
                "allergies": False,
                "campus": "Main",
                "role": 1
            },
            "expected results": False
        },

        "fail signup duplicate email": {
            "params": {
                "username": "test_duplicate_email",
                "password": "Password123",
                "email": "test_existing_user@example.com",
                "first_name": "Test",
                "last_name": "Duplicate",
                "allergies": False,
                "campus": "Main",
                "role": 1
            },
            "expected results": False
        },

        "fail signup missing username": {
            "params": {
                "username": "",
                "password": "Password123",
                "email": "test_missing_username@example.com",
                "first_name": "Test",
                "last_name": "Missing",
                "allergies": False,
                "campus": "Main",
                "role": 1
            },
            "expected results": False
        },

        "fail signup missing password": {
            "params": {
                "username": "test_missing_password",
                "password": "",
                "email": "test_missing_password@example.com",
                "first_name": "Test",
                "last_name": "Missing",
                "allergies": False,
                "campus": "Main",
                "role": 1
            },
            "expected results": False
        },
    }
