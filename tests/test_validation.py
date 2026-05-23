# -------------------------------------------------------------------------------
# filename: app/tests/test_validation.py
# Author: Joseph Egan
# 2026-05-04
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: A testing suite for validation utility functions
# -------------------------------------------------------------------------------

# Local imports
from app.logic.utilities.validation import \
    is_email_or_username, \
    non_empty_string


# ------------------------------ helper classes -------------------------------

class MockEntry:
    """
    Simple object that acts like a Tkinter Entry widget.
    It gives us a .get() method for testing input_string().
    """

    def __init__(self, value: str):
        self.value = value

    def get(self):
        return self.value


# ------------------------------ input_string ---------------------------------

def test_input_string():
    return {
        "input string accepts valid raw string": {
            "params": {
                "entry": "hello",
                "validation_func": non_empty_string
            },
            "expected results": True
        },

        "input string rejects empty raw string": {
            "params": {
                "entry": "",
                "validation_func": non_empty_string
            },
            "expected results": False
        },

        "input string rejects whitespace raw string": {
            "params": {
                "entry": "   ",
                "validation_func": non_empty_string
            },
            "expected results": False
        },

        "input string accepts entry object with valid value": {
            "params": {
                "entry": MockEntry("hello"),
                "validation_func": non_empty_string
            },
            "expected results": True
        },

        "input string rejects entry object with empty value": {
            "params": {
                "entry": MockEntry(""),
                "validation_func": non_empty_string
            },
            "expected results": False
        },

        "input string returns email pattern": {
            "params": {
                "entry": "test@example.com",
                "validation_func": is_email_or_username
            },
            "expected results": (True, "email")
        },

        "input string returns username pattern": {
            "params": {
                "entry": "test_user",
                "validation_func": is_email_or_username
            },
            "expected results": (True, "username")
        },

        "input string returns invalid pattern": {
            "params": {
                "entry": "bad user!",
                "validation_func": is_email_or_username
            },
            "expected results": (False, "invalid")
        },
    }


# ------------------------------ non_empty_string -----------------------------

def test_non_empty_string():
    return {
        "non empty string accepts normal text": {
            "params": {
                "value": "hello"
            },
            "expected results": (True, None)
        },

        "non empty string accepts text with spaces around it": {
            "params": {
                "value": "  hello  "
            },
            "expected results": (True, None)
        },

        "non empty string rejects empty string": {
            "params": {
                "value": ""
            },
            "expected results": (False, None)
        },

        "non empty string rejects whitespace string": {
            "params": {
                "value": "   "
            },
            "expected results": (False, None)
        },

        "non empty string accepts numeric text": {
            "params": {
                "value": "12345"
            },
            "expected results": (True, None)
        },
    }


# ------------------------------ is_email_or_username ------------------------

def test_is_email_or_username():
    return {
        "valid email address": {
            "params": {
                "value": "student@example.com"
            },
            "expected results": (True, "email")
        },

        "valid username letters only": {
            "params": {
                "value": "studentuser"
            },
            "expected results": (True, "username")
        },

        "valid username with numbers": {
            "params": {
                "value": "student123"
            },
            "expected results": (True, "username")
        },

        "valid username with underscore": {
            "params": {
                "value": "student_user"
            },
            "expected results": (True, "username")
        },

        "invalid username with space": {
            "params": {
                "value": "student user"
            },
            "expected results": (False, "invalid")
        },

        "invalid email missing domain": {
            "params": {
                "value": "student@"
            },
            "expected results": (False, "invalid")
        },

        "invalid email missing at symbol": {
            "params": {
                "value": "studentexample.com"
            },
            "expected results": (False, "invalid")
        },
    }


# ------------------------------ is_valid_password ---------------------------

def test_is_valid_password():
    return {
        "valid password exactly eight characters": {
            "params": {
                "value": "12345678"
            },
            "expected results": True
        },

        "valid password longer than eight characters": {
            "params": {
                "value": "Password123"
            },
            "expected results": True
        },

        "invalid password seven characters": {
            "params": {
                "value": "1234567"
            },
            "expected results": False
        },

        "invalid empty password": {
            "params": {
                "value": ""
            },
            "expected results": False
        },

        "valid password with spaces": {
            "params": {
                "value": "pass word"
            },
            "expected results": True
        },
    }


# ------------------------------ validate_passwords_match --------------------

def test_validate_passwords_match():
    return {
        "matching normal passwords": {
            "params": {
                "password": "Password123",
                "confirm_password": "Password123"
            },
            "expected results": True
        },

        "non matching passwords": {
            "params": {
                "password": "Password123",
                "confirm_password": "Password456"
            },
            "expected results": False
        },

        "matching empty passwords": {
            "params": {
                "password": "",
                "confirm_password": ""
            },
            "expected results": True
        },

        "case sensitive password mismatch": {
            "params": {
                "password": "Password123",
                "confirm_password": "password123"
            },
            "expected results": False
        },

        "space sensitive password mismatch": {
            "params": {
                "password": "Password123",
                "confirm_password": "Password123 "
            },
            "expected results": False
        },
    }
