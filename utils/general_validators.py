import phonenumbers
from decouple import config
from flask import request
from werkzeug.exceptions import BadRequest


def validate_password(password):
    special_symbols = ["$", "@", "#", "%", "^", "*", ")", ".", "(", "-", "=", "!", "&", "+"]
    if len(password) < int(config("PASSWORD_MIN_LENGTH")):
        raise BadRequest(
            f"Your password is too short, it needs to have at least {config('PASSWORD_MIN_LENGTH')} characters."
        )

    if len(password) > int(config("PASSWORD_MAX_LENGTH")):
        raise BadRequest(
            f"Your password is too long, it needs to have at most {config('PASSWORD_MAX_LENGTH')} characters."
        )

    if not any(char.isdigit() for char in password):
        raise BadRequest("Your password should have at least one digit.")

    if not any(char.isupper() for char in password):
        raise BadRequest("Your password should have at least one uppercase letter")

    if not any(char.islower() for char in password):
        raise BadRequest("Your password should have at least one lowercase letter")

    if not any(char in special_symbols for char in password):
        raise BadRequest(
            f"Password should have at least one of the special symbols {special_symbols}"
        )


def validate_phone_number(phone_number):
    if "phone" in request.get_json():
        phone = request.get_json()["phone"]
        try:
            if not phonenumbers.is_valid_number(phonenumbers.parse(phone)):
                raise BadRequest(
                    f"The phone number you provided is not valid. Please, provide a valid number in the format '+[country code][number]' or just skip it \N{slightly smiling face}"
                )
        except:
            raise BadRequest(
                f"The phone number you provided is not valid. Please, provide a valid number in the format '+[country code][number]' or just skip it \N{slightly smiling face}"
            )


def validate_tag_length(tags):
    if len(tags) == 0:
        raise BadRequest(
            f"You haven't provided any tags \N{slightly smiling face}"
        )
    for tag in tags:
        if len(tag) > 50 :
            raise BadRequest(
                f"The tag {tag} is too long, please shorten it to up to 50 characters \N{slightly smiling face}"
            )
        if len(tag) == 0:
            raise BadRequest(
                f"You provided an empty string for tag... That's not cool..."
            )