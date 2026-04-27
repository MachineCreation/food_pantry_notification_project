# -------------------------------------------------------------------------------
# filename:LogRecord.py
# Author: Justin Crump
# 2026-04-
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class and Logic for the notification log records

from app.Database.models.t_database import Database

class LogRecord:
    __notification_id = 0
    __date = ""
    __subject = ""
    __message = ""
    __sender = ""
    __recipients = ""

    def __init__(self, notification_id, date, subject, message,
                 sender, recipients):
        self.__notification_id = notification_id
        self.__date = date
        self.__subject = subject
        self.__message = message
        self.__sender = sender
        self.__recipients = recipients

    def get_notification_id(self):
        return self.__notification_id

    def get_date(self):
        return self.__date

    def get_subject(self):
        return self.__subject

    def get_message(self):
        return self.__message

    def get_sender(self):
        return self.__sender

    def get_recipients(self):
        return self.__recipients

    @staticmethod
    def search():
        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT  NOTIFICATIONS.notification_id,
                NOTIFICATIONS.date_time,
                NOTIFICATIONS.subject,
                NOTIFICATIONS.body_text,
                NOTIFICATIONS.sender_id,
                NOTIFICATIONS.num_recip
        FROM    NOTIFICATIONS
        """)

        results = cursor.fetchall()

        log_list = []

        for row in results:
            log = LogRecord(row[0], row[1], row[2], row[3], row[4], row[5])
            log_list.append(log)

        conn.close()
        print("Connection closed")

        return log_list


