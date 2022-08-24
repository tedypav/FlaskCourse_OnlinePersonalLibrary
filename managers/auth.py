from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import Unauthorized

from models import UserModel


class AuthManager:
    """
    A class responsible for the authentication to the library.
    """

    @staticmethod
    def encode_token(user):
        """
        Creates a valid token. It takes the user, extracts the user ID, combines it with the random JWT_SECRET from
        the .env file and adds information about the expiration date of the token.

        :param user: user trying to register or log in
        :return: token: string, a valid token
        """
        payload = {
            "sub": user.user_id,
            "exp": datetime.utcnow()
            + timedelta(minutes=int(config("TOKEN_VALIDITY_VALUE_IN_MINUTES"))),
        }
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        """
        Decodes the encoded token. If it's valid, returns the user ID. If it's invalid, returns a message
        with what exactly is the problem in the token.

        :param token: string; a token previously provided to the user
        :return: user_id: int
        """
        if not token:
            raise Unauthorized(
                "You need a token to get access to this endpoint \N{winking face}"
            )
        try:
            payload = jwt.decode(token, key=config("JWT_SECRET"), algorithms=["HS256"])
            return payload["sub"]
        except ExpiredSignatureError:
            raise Unauthorized("Sorry, your token has expired. Please, log in again.")
        except InvalidTokenError:
            raise Unauthorized(
                "Sorry, your token is invalid \N{unamused face}. Please, register or login again to obtain a valid token."
            )


auth = HTTPTokenAuth()


@auth.verify_token
def verify(token):
    """
    Verifies that the provided token is valid and hasn't expired yet.

    :param token: string; a token previously provided to the user
    :return: user: the user information from the user table
    """
    user_id = AuthManager.decode_token(token)
    return UserModel.query.filter_by(user_id=user_id).first()
