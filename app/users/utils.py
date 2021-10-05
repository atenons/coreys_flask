import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from app import mail


# generate new file name for profile picture to avoid collision and save to app/static/.. directory with resize
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics", picture_filename
    )

    output_size = (125, 125)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)

    if current_user.image_file != "default.jpg":
        try:
            current_picture_path = os.path.join(
                current_app.root_path, "static/profile_pics", current_user.image_file
            )
            os.remove(current_picture_path)
        except Exception:
            pass

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Request Password Reset",
        sender=current_app.config["MAIL_SENDER"],
        recipients=[user.email],
    )
    msg.body = f"""To reset your password,visit the following link 
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email."""
    mail.send(msg)
