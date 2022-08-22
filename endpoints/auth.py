from decouple import config
from flask import request
from flask_api import status
from flask_restful import Resource

from managers.user import UserManager
from schemas.request.auth import LoginSchemaRequest, RegisterSchemaRequest
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(RegisterSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.register(data)
        return {
            "message": f"Welcome to our library! This token will only be valid for the next {config('TOKEN_VALIDITY_VALUE_IN_MINUTES')} minutes. After that you'll need to log in \N{winking face}",
            "token": token,
        }, status.HTTP_201_CREATED


class LoginResource(Resource):
    @validate_schema(LoginSchemaRequest)
    def post(self):
        data = request.get_json()
        token = UserManager.login(data)
        return {
            "message": f"This token will only be valid for the next {config('TOKEN_VALIDITY_VALUE_IN_MINUTES')} minutes. After that you'll need to log in again \N{winking face}",
            "token": token,
        }, status.HTTP_200_OK
