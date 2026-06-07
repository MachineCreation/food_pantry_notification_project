# from app.database.models.Notifier import Notifier
from app.logic.models.Notification import Notification


def test_send_sms_otp():
    '''
    test the send_sms_otp method of the Notifier class
    '''
    recipient = [1, 1234567890]
    otp = Notification.send_sms_otp(recipient)

    print(f"OTP sent: {otp}")


if __name__ == "__main__":
    test_send_sms_otp()