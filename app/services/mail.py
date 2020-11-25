from flask import current_app
from flask_mail import Message
import os

sender = os.environ.get('MAIL_USERNAME')


def sendEmail(subject, body, recipient):
    msg = Message(subject, sender=sender, recipients=[recipient])

    msg.body = body

    current_app.mail.send(msg)
