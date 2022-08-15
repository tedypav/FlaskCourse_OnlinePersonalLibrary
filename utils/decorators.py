from flask import request
from werkzeug.exceptions import BadRequest, Forbidden
from decouple import config

from managers.auth import auth
import phonenumbers


def validate_schema(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)
        return wrapper
    return decorated_function


def permission_required(role):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.role == role:
                raise Forbidden("You do not have the necessary permissions to access this information \N{unamused face}")
            return func(*args, **kwargs)
        return wrapper
    return decorated_function


def validate_password(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            password = request.get_json()["password"]

            special_symbols = ["$", "@", "#", "%", "^", "*", ")", ".", "(", "-", "="]
            if len(password) < int(config("PASSWORD_MIN_LENGTH")):
                raise BadRequest(f"Your password is too short, it needs to have at least {config('PASSWORD_MIN_LENGTH')} characters.")

            if len(password) > int(config("PASSWORD_MAX_LENGTH")):
                raise BadRequest(f"Your password is too long, it needs to have at most {config('PASSWORD_MAX_LENGTH')} characters.")

            if not any(char.isdigit() for char in password):
                raise BadRequest("Your password should have at least one digit.")

            if not any(char.isupper() for char in password):
                raise BadRequest("Your password should have at least one uppercase letter")

            if not any(char.islower() for char in password):
                raise BadRequest("Your password should have at least one lowercase letter")

            if not any(char in special_symbols for char in password):
                raise BadRequest(f"Password should have at least one of the special symbols {special_symbols}")
            return func(*args, **kwargs)
        return wrapper
    return decorated_function


def validate_phone_number(schema_name):
    def decorated_function(func):
        def wrapper(*args, **kwargs):
            if "phone" in request.get_json():
                phone = request.get_json()["phone"]
                try:
                    if phonenumbers.is_valid_number(phonenumbers.parse(phone)) == False:
                        raise BadRequest(
                            f"The phone number you provided is not valid. Please, provide a valid number in the format '+[country code][number]' or just skip it \N{slightly smiling face}")
                except:
                    raise BadRequest(
                        f"The phone number you provided is not valid. Please, provide a valid number in the format '+[country code][number]' or just skip it \N{slightly smiling face}")
            return func(*args, **kwargs)
        return wrapper
    return decorated_function

