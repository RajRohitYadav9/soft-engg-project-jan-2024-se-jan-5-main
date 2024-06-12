from backend.application.tasks import async_send_email, send_reminder

def test_async_send_email():
    data = {
        "username": "Parag123",
        "ticket_id": "3",
        "email": "xyzporag0000@gmail.com"
    }
    res = async_send_email(to=[data],sub="testing broo",priority=None)
    assert res == 200

def test_async_gchat_notification():
    res = send_reminder()
    assert res == 200