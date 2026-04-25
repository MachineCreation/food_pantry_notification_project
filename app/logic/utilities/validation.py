#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/logic/utilities/validations.py
# Author: Joseph Egan
# 2026-04-24
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: basic validation functions for the application

# Local imports

# python imports
from typing import Callable, Tuple


# ------------------------------ input validations ----------------------------
def input_string(entry: object, validation_func: Callable) -> \
        bool | Tuple[bool, str]:
    '''
    validation function for string input in entry fields
    :param entry: the entry field to validate
    :param validation_func: the function to use for validation
    :return: True if valid, False otherwise
    '''
    if isinstance(entry, str):
        value = entry
    elif hasattr(entry, "get"):
        value = entry.get()
    else:
        raise ValueError("Invalid entry type. Must be a string or an object "
                         "with a get() method.")

    valid, return_param = validation_func(value)
    if return_param is None:
        return valid
    return valid, return_param


# -------------------------- validation functions -----------------------------
def non_empty_string(value: str) -> Tuple[bool, None]:
    '''
    validation function for non-empty string input
    :param value: the string to validate
    :return: True if valid, False otherwise
    '''
    return bool(value and value.strip()), None


# --------------------
def is_email_or_username(value: str) -> Tuple[bool, str]:
    '''
    validation function for email or username input
    :param value: the string to validate
    :return: bool, string bool:True if valid, False otherwise,
        string 'email' | 'username'
    '''
    import re
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    username_pattern = r'^[a-zA-Z0-9_]+$'
    valid = bool(re.match(email_pattern, value) or
                 re.match(username_pattern, value))
    pattern = ('email' if re.match(email_pattern, value) else 'username' if
               re.match(username_pattern, value) else 'invalid')
    return valid, pattern


# --------------------
def is_valid_password(value: str) -> Tuple[bool, None]:
    '''
    validation function for password input
    :param value: the string to validate
    :return: True if valid, False otherwise
    '''
    return len(value) >= 8


# --------------------
def validate_passwords_match(password: str, confirm_password: str) -> \
        Tuple[bool, None]:
    '''
    validation function for matching password and confirm password fields
    :param password: the password to validate
    :param confirm_password: the confirm password to validate
    :return: True if valid, False otherwise
    '''
    return password == confirm_password
