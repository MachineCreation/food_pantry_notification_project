#! /usr/bin/env python3.14
# -------------------------------------------------------------------------------
# filename: app/database/models/Notifier.py
# Author: Joseph Egan
# 2026-05-15
# Sources:
# Contributors:
# -------------------------------------------------------------------------------
# Description: Class that handles sending notifications via email
# Note: later will send via sms as well

# Local imports
import env

# python imports
from typing import List
from email.message import EmailMessage
import smtplib
import markdown
import requests


class Notifier():

    def __init__(self):
        self.__gmail = env.GMAIL
        self.__gmail_key = env.GMAIL_KEY
        self.__dev_email = env.DEV_EMAIL
        self.connect()

# --------------------------------- connections -------------------------------
    def connect(self) -> None:
        '''
        create a temporary connection to gmail with smtp
        :return connection: email provider connection
            !!! You must always disconnect the provider connection when not
            in use! It poses a real security concern when left open and
            unmonitored !!!
        '''
        self.__connection: smtplib.SMTP_SSL = \
            smtplib.SMTP_SSL("smtp.gmail.com", 465)
        connected = self.__connection.login(self.__gmail, self.__gmail_key)
        if not connected:
            raise ConnectionError

    # --------------------
    def disconnect(self) -> None:
        '''
        Disconnect the email provider
        '''
        if self.__connection:
            self.__connection.quit()
            self.__connection = None

# --------------------------------- methods ---------------------------------
    def process_emails(
            self,
            date: str,
            subject: str,
            message: str,
            recipient: str,
            campuses: List[str] | None = None
    ) -> bool:
        '''
        send emails to listed recipients
        :param subject: string subject of the email
        :param message: string message content of the email
        :param recipient: string email address to send the email to
        :return: boolean indicating success or failure of the email sending
            operation
        '''

        try:
            if not self.__connection:
                self.connect()

            if self.__dev_email:
                recipient = self.__dev_email

            if not all([subject, message, recipient]):
                raise ValueError()

            # compose email body
            md_email, plain_email = self.compose_md_email(
                date,
                subject,
                message,
                campuses
            )

            # send emails
            self.send_email(
                recipient,
                subject,
                plain_email,
                md_email
            )

            # disconnect and return
            self.disconnect()
            return True

        except (ValueError or KeyError) as e:
            self.disconnect()
            print(f'{e.__str__}'
                  'Value or key error on Notifier.process_emails()\n')
            return False

        except smtplib.SMTPException as e:
            print(f'{e.strerror}'
                  'Connection error on Notifier.process_emails()\n')
            return False

    # --------------------
    def process_sms(
            self,
            subject: str,
            message: str,
            recipient: str
    ) -> bool:
        '''
        send sms to listed recipients using textbelt API
        :param subject: string subject of the sms
        :param message: string message content of the sms
        :param recipient: list of str phone number and int user id to send the
            sms to
        :return: boolean indicating success or failure of the sms sending
            operation
        '''

        try:
            if not all([subject, message, recipient]):
                raise ValueError()

            self.send_SMS(recipient, f'{subject}\n{message}')

            # disconnect and return
            return True

        except (ValueError or KeyError) as e:
            print(f'{e}'
                  'Value or key error on Notifier.process_sms()\n')
            return False

    # --------------------
    def compose_md_email(
            self,
            date: str,
            subject: str,
            message: str,
            campuses: List[str] | None
    ) -> str:
        '''
        compose an email in md format
        :param date: datetime string
        :param subject: string subject of email
        :param message: string message body of email
        :return: formatted email ready to send
        '''

        if campuses:
            campuses_string = f'''
##Campuses

{"\n*".join(campuses)}
'''
        body_text = f'''
{date}
#{subject}

{message}
{campuses_string if campuses else ""}
'''
        md_body = markdown.markdown(
            body_text,
            extensions=["extra", "nl2br", "sane_lists"]
        )

        return md_body, body_text

    # --------------------
    def send_email(
            self,
            recipient: str,
            subject: str,
            plain_body: str,
            md_body: str,
    ) -> None:
        '''
        send an email
        :return: None else smtp.SMTPException is raised
        '''

        msg = EmailMessage()
        msg["From"] = \
            f"Food Pantry Notification Project - No-Reply <{self.__gmail}>"
        msg["To"] = recipient
        msg["Subject"] = subject

        # Plain-text fallback
        msg.set_content(plain_body)

        # HTML version rendered from Markdown
        msg.add_alternative(md_body, subtype="html")

        self.__connection.send_message(msg)
        del msg

    # --------------------
    def send_SMS(
            self,
            recipient: str,
            message: str
    ) -> None:
        '''
        send an sms message to a recipient using textbelt API
        :param recipient: str phone number of the recipient
        :param message: string message content of the sms
        :return: None else ValueError is raised
        '''

        key = env.TEXTBELT_KEY
        # send sms via textbelt API
        resp = requests.post('https://textbelt.com/text', {
            'phone': recipient,
            'message': message,
            'key': key,
        })

        if not resp.json().get('success'):
            raise ValueError(f'SMS not sent to {recipient}')

# --------------------------------- STATIC -------------------------------
    @staticmethod
    def send_SMS_otp(
            recipient: str
    ) -> str:
        '''
        send sms messages to listed recipients using textbelt API
        :param recipient: a string containing the recipient's phone number
        '''

        key = env.TEXTBELT_KEY
        # send sms via textbelt API
        try:
            otp_request = requests.post('https://textbelt.com/otp/generate', {
                'phone': recipient,
                'userid': 'otp_user',
                'key': key,
            })
            otp = otp_request.json().get('otp')
            if not otp:
                raise ValueError('OTP not generated')
        except (ValueError or requests.RequestException) as e:
            print(f'{e}\n'
                  'Error on Notifier.send_SMS_otp()\n')
            return None

        return otp
