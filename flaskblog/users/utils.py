import os
import secrets

from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from PIL import Image

from flaskblog import mail


def save_avatar(form_avatar):
    random_hex = secrets.token_hex(10)
    _, extension = os.path.splitext(form_avatar.filename)
    avatar_filename = random_hex + extension
    avatar_path = os.path.join(current_app.root_path, 'static/images/account', avatar_filename)

    avatar_size = (125, 125)
    i = Image.open(form_avatar)
    i.thumbnail(avatar_size)

    i.save(avatar_path)

    if 'default.png' not in current_user.avatar:
        avatar_path_previous = os.path.join(current_app.root_path, 'static/images/account', current_user.avatar)
        if os.path.isfile(avatar_path_previous):
            os.remove(avatar_path_previous)

    return avatar_filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject='Password Reset Request', sender='dataflow@ukr.net', recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}
    
    If you did not make this request, then simply ignore this email and no changing will be made.'''
    mail.send(msg)
