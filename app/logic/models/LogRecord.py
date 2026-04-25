# -------------------------------------------------------------------------------
# filename:LogRecord.py
# Author: Justin Crump
# 2026-04-
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class and Logic for the notification log records

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

    @classmethod
    def search(cls):
        from app.Database.models.fake_data import FakeData
        all_data = FakeData.get_fake_data
        return all_data
