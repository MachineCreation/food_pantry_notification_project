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
import re


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
    else:
        getter = getattr(entry, "get", None)
        if callable(getter):
            value = getter()
        else:
            raise ValueError(
                "Invalid entry type. Must be a string or an object "
                "with a get() method."
            )

    valid, return_param = validation_func(value)
    return valid if return_param is None else (valid, return_param)


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
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    username_pattern = r'^[a-zA-Z0-9_]+$'
    valid = bool(re.match(email_pattern, value) or
                 re.match(username_pattern, value))
    pattern = ('email' if re.match(email_pattern, value) else 'username' if
               re.match(username_pattern, value) else 'invalid')
    return valid, pattern


# --------------------
def is_name(value: str) -> Tuple[bool, None]:
    '''
    evaluates if the string entry is in name format
    :param value: the string to validate
    :return: True if valid, False otherwise
    '''
    name_pattern = r'^[A-Za-z-]+$'
    return bool(re.match(name_pattern, value)), None


# --------------------
def is_password_length(password: str) -> bool:
    '''
    validation function for password input
    :param password: the string to validate
    :return: True if valid, False otherwise
    '''
    return len(password) >= 8


# --------------------
def password_has_uppercase(password: str) -> bool:
    '''
    :return boolean: return true if password has an uppercase letter
        else return False
    '''
    uppercase = any(char.isupper() for char in password)
    return uppercase


# --------------------
def password_has_lowercase(password: str) -> bool:
    '''
    :return boolean: return true if password has a lowercase letter
        else return False
    '''
    lowercase = any(char.islower() for char in password)
    return lowercase


# --------------------
def password_has_digit(password: str) -> bool:
    '''
    :return boolean: return true if password has a digit
        else return False
    '''
    digit = any(char.isdigit() for char in password)
    return digit


# --------------------
def password_has_special_char(password: str) -> bool:
    '''
    :return boolean: return true if password has a special character
        else return False
    '''
    special_char = any(not char.isalnum() for char in password)
    return special_char


# --------------------
def no_spaces(value: str) -> bool:
    '''
    :return bool: return True if there are no spaces in the stirng
        else return False
    '''
    spaces = any(char.isspace() for char in value)
    return not spaces


# --------------------
def validate_passwords_match(password: str, confirm_password: str) -> \
        bool:
    '''
    validation function for matching password and confirm password fields
    :param password: the password to validate
    :param confirm_password: the confirm password to validate
    :return: True if valid, False otherwise
    '''
    return password == confirm_password
