import os
import secrets
from PIL import Image, ImageStat
from flask import url_for, current_app
from flask_mail import Message
from recipes2 import mail


def save_picture(form_picture, folder):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, f'static/{folder}', picture_fn)
    duplicate = check_for_duplicate(form_picture,os.path.join(current_app.root_path, f'static/{folder}'))
    if duplicate:
        return duplicate
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail=output_size
    i.save(picture_path)
    return(picture_fn)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender=os.environ['EMAIL_USER'], recipients=[user.email])
    print("send_reset_token is sending an email to: ", user.email)
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request please ignore this email and no changes will be made.
'''
    mail.send(msg)

def check_for_duplicate(picture,folder):
    new_image = Image.open(picture)
    pix_mean1 = ImageStat.Stat(new_image).mean
    images = [ _ for _ in os.listdir(folder)]
    for pic in images:
        compare_img =  Image.open(os.path.join(folder, pic))
        pix_mean2 = ImageStat.Stat(compare_img).mean

        if pix_mean1 == pix_mean2:
            return pic
    return False