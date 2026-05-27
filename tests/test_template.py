# -------------------------------------------------------------------------------
# filename: app/tests/test_template.py
# Author: Lloyd Truong
# 2026-05-23
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description:

import unittest
from unittest.mock import MagicMock

from app.logic.models.Template_logic import TemplateLogic


class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.mock_db = MagicMock()
        self.logic = TemplateLogic(self.mock_db)

    def test_get_existing_template_names_returns_names(self):
        """
        checks that the logic returns the template names correctly
        when the database has existing rows
        """
        self.mock_db.execute_query.return_value = [
            ("WelcomeTemplate",),
            ("AlertTemplate",),
            ("ServiceTemplate",),
        ]

        result = self.logic.get_existing_template_names()

        self.assertEqual(
            result,
            ["WelcomeTemplate", "AlertTemplate", "ServiceTemplate"]
        )

    def test_get_existing_template_names_returns_empty_list(self):
        """
        checks that the logic gives back an empty list
        when there are no templates in the database
        """
        self.mock_db.execute_query.return_value = []

        result = self.logic.get_existing_template_names()

        self.assertEqual(result, [])

    def test_get_template_details_returns_selected_template(self):
        """
        checks that the selected template details are returned correctly from the database
        """
        self.mock_db.execute_query.return_value = (
            "WelcomeTemplate",
            "Welcome to our service",
            "General Update",
            "We are glad to have you here."
        )

        result = self.logic.get_template_details("WelcomeTemplate")

        self.assertEqual(
            result,
            (
                "WelcomeTemplate",
                "Welcome to our service",
                "General Update",
                "We are glad to have you here."
            )
        )

    def test_get_template_details_returns_none_when_not_found(self):
        """
        checks that the logic returns None if the selected template does not exist
        """
        self.mock_db.execute_query.return_value = None

        result = self.logic.get_template_details("MissingTemplate")

        self.assertIsNone(result)

    def test_save_template_and_message_updates_existing_template(self):
        """
        should update an existing template if template_name already exists
        """
        self.mock_db.execute_query.side_effect = [
            (5,),  # existing template found
            None,  # update query
            None  # extra query if your logic calls execute_query again
        ]

        result = self.logic.save_template_and_message(
            template_name="WelcomeTemplate",
            subject="Updated Subject",
            tags="General Update",
            message="Updated body text",
            creator_id=1
        )

        self.assertEqual(result, 5)
        self.assertGreaterEqual(self.mock_db.execute_query.call_count, 2)

    def test_save_template_and_message_inserts_new_template(self):
        """
        checks that the logic inserts a new template
        when the template name is not already in the database
        """
        self.mock_db.execute_query.side_effect = [
            None,   # template not found
            None,   # insert runs
            (8,)    # new template id found
        ]

        result = self.logic.save_template_and_message(
            template_name="NewTemplate",
            subject="New Subject",
            tags="Date",
            message="New body text",
            creator_id=1
        )

        self.assertEqual(result, 8)
        self.assertGreaterEqual(self.mock_db.execute_query.call_count, 3)


if __name__ == "__main__":
    unittest.main()
