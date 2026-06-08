# from app.database.models.Notifier import Notifier
from app.database.models.Database import Database


def test_send_sms_otp():
    '''
    test the send_sms_otp method of the Notifier class
    '''
    db = Database()
    res = db.get_recipients()
    print(res)


if __name__ == "__main__":
    test_send_sms_otp()