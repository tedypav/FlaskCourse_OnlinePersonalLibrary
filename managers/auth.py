from datetime import datetime, timedelta
import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import ExpiredSignatureError, InvalidTokenError
from werkzeug.exceptions import Unauthorized

from models import UserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.user_id,
            "exp": datetime.utcnow() + timedelta(minutes=int(config('TOKEN_VALIDITY_VALUE_IN_MINUTES')))
        }
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        if not token:
            raise Unauthorized("You need a token to get access to this endpoint \N{winking face}")
        try:
            payload = jwt.decode(token, key=config("JWT_SECRET"), algorithms=["HS256"])
            return payload["sub"]
        except ExpiredSignatureError:
            raise Unauthorized("Sorry, your token has expired. Please, log in again.")
        except InvalidTokenError:
            raise Unauthorized("Sorry, your token is invalid \N{unamused face}. Please, register or login again to obtain a valid token.")


auth = HTTPTokenAuth()


@auth.verify_token
def verify(token):
    user_id = AuthManager.decode_token(token)
    return UserModel.query.filter_by(user_id=user_id).first()

