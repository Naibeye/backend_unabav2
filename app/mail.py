
from flask_mail import Message
from threading import Thread
from flask import current_app
from . import mail

def send_async_email(app, to, subject, template, **kwargs):
    with app.app_context():  # pragma: no cover
        msg = Message(subject=subject, sender=('Naibi SSO Authentication','noreply@naibi.io'), recipients=[to])
        msg.html = template
        mail.send(msg)


def send_email(to, subject, template, **kwargs):  # pragma: no cover
    app = current_app._get_current_object()
    # send_async_email(app, to, subject, template)
    thread = Thread(
        target=send_async_email, args=(app, to, subject, template), kwargs=kwargs
    )
    thread.start()
    return thread 
