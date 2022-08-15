from datetime import datetime, timedelta
import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth

from models import UserModel


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.user_id,
            "exp": datetime.utcnow() + timedelta(minutes=int(config('TOKEN_VALIDITY_VALUE_IN_MINUTES')))
        }
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")


auth = HTTPTokenAuth()


@auth.verify_token
def verify(token):
    user_id = AuthManager.decode_token(token)
    return UserModel.query.filter_by(user_id=user_id).first()

