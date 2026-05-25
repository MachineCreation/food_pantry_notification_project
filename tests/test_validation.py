# -------------------------------------------------------------------------------
# filename: app/tests/test_validation.py
# Author: Joseph Egan
# 2026-05-04
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: unittest suite for validation utility functions
# -------------------------------------------------------------------------------

import unittest

from app.logic.utilities.validation import (
    input_string,
    is_email_or_username,
    is_password_length,
    non_empty_string,
    validate_passwords_match,
)


class MockEntry:
    """
    Simple object that acts like a Tkinter Entry widget.
    It gives us a .get() method for testing input_string().
    """

    def __init__(self, value: str):
        self.value = value

    def get(self):
        return self.value


class TestValidation(unittest.TestCase):
    # ------------------------------ input_string ---------------------------------

    def test_input_string_accepts_valid_raw_string(self):
        self.assertTrue(input_string("hello", non_empty_string))

    def test_input_string_rejects_empty_raw_string(self):
        self.assertFalse(input_string("", non_empty_string))

    def test_input_string_rejects_whitespace_raw_string(self):
        self.assertFalse(input_string("   ", non_empty_string))

    def test_input_string_accepts_entry_object_with_valid_value(self):
        self.assertTrue(input_string(MockEntry("hello"), non_empty_string))

    def test_input_string_rejects_entry_object_with_empty_value(self):
        self.assertFalse(input_string(MockEntry(""), non_empty_string))

    def test_input_string_returns_email_pattern(self):
        self.assertEqual(
            input_string("test@example.com", is_email_or_username),
            (True, "email"),
        )

    def test_input_string_returns_username_pattern(self):
        self.assertEqual(
            input_string("test_user", is_email_or_username),
            (True, "username"),
        )

    def test_input_string_returns_invalid_pattern(self):
        self.assertEqual(
            input_string("bad user!", is_email_or_username),
            (False, "invalid"),
        )

    # ------------------------------ non_empty_string -----------------------------

    def test_non_empty_string_accepts_normal_text(self):
        self.assertEqual(non_empty_string("hello"), (True, None))

    def test_non_empty_string_accepts_text_with_spaces_around_it(self):
        self.assertEqual(non_empty_string("  hello  "), (True, None))

    def test_non_empty_string_rejects_empty_string(self):
        self.assertEqual(non_empty_string(""), (False, None))

    def test_non_empty_string_rejects_whitespace_string(self):
        self.assertEqual(non_empty_string("   "), (False, None))

    def test_non_empty_string_accepts_numeric_text(self):
        self.assertEqual(non_empty_string("12345"), (True, None))

    # ------------------------------ is_email_or_username ------------------------

    def test_is_email_or_username_valid_email_address(self):
        self.assertEqual(is_email_or_username("student@example.com"), (True, "email"))

    def test_is_email_or_username_valid_username_letters_only(self):
        self.assertEqual(is_email_or_username("studentuser"), (True, "username"))

    def test_is_email_or_username_valid_username_with_numbers(self):
        self.assertEqual(is_email_or_username("student123"), (True, "username"))

    def test_is_email_or_username_valid_username_with_underscore(self):
        self.assertEqual(is_email_or_username("student_user"), (True, "username"))

    def test_is_email_or_username_invalid_username_with_space(self):
        self.assertEqual(is_email_or_username("student user"), (False, "invalid"))

    def test_is_email_or_username_invalid_email_missing_domain(self):
        self.assertEqual(is_email_or_username("student@"), (False, "invalid"))

    def test_is_email_or_username_invalid_email_missing_at_symbol(self):
        self.assertEqual(is_email_or_username("studentexample.com"), (False, "invalid"))

    # ------------------------------ is_password_length ---------------------------

    def test_is_password_length_valid_password_exactly_eight_characters(self):
        self.assertTrue(is_password_length("12345678"))

    def test_is_password_length_valid_password_longer_than_eight_characters(self):
        self.assertTrue(is_password_length("Password123"))

    def test_is_password_length_invalid_password_seven_characters(self):
        self.assertFalse(is_password_length("1234567"))

    def test_is_password_length_invalid_empty_password(self):
        self.assertFalse(is_password_length(""))

    def test_is_password_length_valid_password_with_spaces(self):
        self.assertTrue(is_password_length("pass word"))

    # ------------------------------ validate_passwords_match --------------------

    def test_validate_passwords_match_matching_normal_passwords(self):
        self.assertTrue(validate_passwords_match("Password123", "Password123"))

    def test_validate_passwords_match_non_matching_passwords(self):
        self.assertFalse(validate_passwords_match("Password123", "Password456"))

    def test_validate_passwords_match_matching_empty_passwords(self):
        self.assertTrue(validate_passwords_match("", ""))

    def test_validate_passwords_match_case_sensitive_password_mismatch(self):
        self.assertFalse(validate_passwords_match("Password123", "password123"))

    def test_validate_passwords_match_space_sensitive_password_mismatch(self):
        self.assertFalse(validate_passwords_match("Password123", "Password123 "))


if __name__ == "__main__":
    unittest.main(verbosity=2)
