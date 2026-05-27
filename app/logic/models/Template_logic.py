# -------------------------------------------------------------------------------
# filename: template.py
# Author: Lloyd Truong
# 2026-05-10
# Sources: None
# Contributors:
# -------------------------------------------------------------------------------

class TemplateLogic:
    """
    Handles database-related logic for the Template Creation feature.
    """
    def __init__(self, database):
        """
        Initializes the TemplateLogic with a database instance.
        :param database: active Database object used for SQL queries
        """
        self.__db = database

    def get_existing_template_names(self):
        """
        Returns all template names from the TEMPLATE table.

        :return: list of template name strings
        """
        rows = self.__db.execute_query(
            "SELECT template_name FROM TEMPLATE ORDER BY created_date DESC;",
            fetch_all=True
        )
        return [row[0] for row in rows] if rows else []

    def get_template_details(self, template_name):
        """
        returns template name, subject, tags, and the most recent body_text
        associated with the selected template.
        :param template_name: selected template name
        """
        row = self.__db.execute_query(
            """
            SELECT
                template_name,
                subject,
                tags,
                template_body
            FROM TEMPLATE
            WHERE template_name = %s;
            """,
            (template_name,),
            fetch_all=False
        )
        return row

    def save_template_and_message(self, template_name, subject, tags, message, creator_id=1):
        """
        Saves template data to TEMPLATE and message body to NOTIFICATIONS.
        :param template_name: template name
        :param subject: subject line
        :param tags: tag string
        :param message: body text
        :param creator_id: placeholder creator ID for now
        :return: template_id
        """
        existing_template = self.__db.execute_query(
            """
            SELECT template_id
            FROM TEMPLATE
            WHERE template_name = %s;
            """,
            (template_name,),
            fetch_all=False
        )

        if existing_template:
            template_id = existing_template[0]

            self.__db.execute_query(
                """
                UPDATE TEMPLATE
                SET subject = %s,
                    tags = %s,
                    template_body = %s
                WHERE template_id = %s;
                """,
                (subject, tags, message, template_id),
                fetch_all=False
            )
        else:
            self.__db.execute_query(
                """
                INSERT INTO TEMPLATE
                    (template_name, creator_id, subject, template_body, tags, created_date)
                VALUES
                    (%s, %s, %s, %s, %s, GETDATE());
                """,
                (template_name, creator_id, subject, message, tags),
                fetch_all=False
            )

            new_row = self.__db.execute_query(
                """
                SELECT template_id
                FROM TEMPLATE
                WHERE template_name = %s;
                """,
                (template_name,),
                fetch_all=False
            )
            template_id = new_row[0]

        return template_id