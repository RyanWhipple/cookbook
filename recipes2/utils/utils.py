import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from recipes2 import mail


def save_picture(form_picture,folder='profile_pics'):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, f"static/{folder}", picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail=output_size
    i.save(picture_path)
    return(picture_fn)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='ryan_whipple@icloud.com', recipients=[user.email])
    print("send_reset_token is sending an email to: ", user.email)
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request please ignore this email and no changes will be made.
'''
    mail.send(msg)