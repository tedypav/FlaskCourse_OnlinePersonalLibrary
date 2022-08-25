from decouple import config
from flask import request
from flask_api import status
from flask_restful import Resource

from managers.user import UserManager
from schemas.request.auth import LoginSchemaRequest, RegisterSchemaRequest
from utils.decorators import validate_schema


class RegisterResource(Resource):
    """
    A resource for initial user registration. Validates that the provided data matches the requested schema, then creates
    a record in the user table. If everything is okay, returns a happy message, 201 CREATED and a valid token.

    Headers: "Content-Type": "application/json"
    Body: first_name (mandatory; a string between 1 and 30 characters)
          last_name (mandatory; a string between 1 and 30 characters)
          email (mandatory; a valid e-mail address)
          password (mandatory; needs to have at least 6 characters, at least 1 lowercase letter,
                     at least 1 capital letter, at least 1 digit, at least 1 special symbol of the
                     following: ["$", "@", "#", "%", "^", "*", ")", ".", "(", "-", "=", "!", "&", "+"])
          phone (optional; a valid phone number of the format "+[country code][phone number]")
          company (optional; a string between 1 and 50 characters)
          job_position (optional; a string between 1 and 50 characters)
    """

    @validate_schema(RegisterSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {
            "message": f"Welcome to our library! This token will only be valid for the next {config('TOKEN_VALIDITY_VALUE_IN_MINUTES')} minutes. After that you'll need to log in \N{winking face}",
            "token": token,
        }, status.HTTP_201_CREATED


class LoginResource(Resource):
    """
    A resource for user login. Validates that the provided data matches the requested schema.
    If everything is okay, returns a happy message, 200 OK and a valid token.

    Headers: "Content-Type": "application/json"
    Body: email (mandatory; the e-mail you registered with)
          password (mandatory; the password you registered with)
    """

    @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {
            "message": f"This token will only be valid for the next {config('TOKEN_VALIDITY_VALUE_IN_MINUTES')} minutes. After that you'll need to log in again \N{winking face}",
            "token": token,
        }, status.HTTP_200_OK
