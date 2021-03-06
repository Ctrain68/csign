from flask import url_for, current_app
from src import mail
from flask_mail import Message
import secrets
import os
from PIL import Image
import qrcode
import re


def strip_chars(business_name):
    regex = re.compile("[A-Za-z0-9]")
    return_matched = regex.findall(business_name)
    return ''.join(return_matched).lower()


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    #form_picture.save(picture_path)

    return picture_fn


def generate_qr(business_name):
    img = qrcode.make('http://c-sign.in/signin/' + strip_chars(business_name))
    random_hex = secrets.token_hex(8)
    picture_fn = business_name + random_hex + '.png'
    picture_path = os.path.join(current_app.root_path, 'static/qr_codes', picture_fn)
    img.save(picture_path)

    return picture_fn


def send_qr_email():
    pass


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then ignore this email.    
    '''
    mail.send(msg)