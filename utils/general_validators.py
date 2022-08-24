import phonenumbers
from decouple import config
from flask import request
from werkzeug.exceptions import BadRequest


def validate_password(password):
    """
    Validates that the password meets the requirements for min/max length, types of symbols (lowercase and uppercase
    letter), at least one digit, at least one special symbol (it also defines special symbols).

    :param password: string; password, provided by the user
    :return Nothing, if the password is valid; BadRequest, if the password is invalid
    """
    special_symbols = [
        "$",
        "@",
        "#",
        "%",
        "^",
        "*",
        ")",
        ".",
        "(",
        "-",
        "=",
        "!",
        "&",
        "+",
    ]
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
    """
    Validate that the provided phone number is valid.

    :param phone_number: string; the phone number, provided by the user
    :return Nothing, if the phone number is valid; BadRequest, if the phone number is invalid

    """
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
    """
    Ensures that a tags are provided.
    Ensures that each tag is in the requested length.

    :param tags: list of tags (strings)
    :return Nothing, if every tag of the list is of the requested length; BadRequest, if the length of any of the tags doesn't meet the requirements
    """

    # Check that any tags were provided
    if len(tags) == 0:
        raise BadRequest(f"You haven't provided any tags \N{slightly smiling face}")

    # Check each tag's length
    for tag in tags:
        if len(tag) > 50:
            raise BadRequest(
                f"The tag {tag} is too long, please shorten it to up to 50 characters \N{slightly smiling face}"
            )
        if len(tag) == 0:
            raise BadRequest(
                f"You provided an empty string for tag... That's not cool..."
            )
