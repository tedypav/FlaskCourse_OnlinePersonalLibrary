from datetime import datetime, timedelta
import jwt
from decouple import config


class AuthManager:
    @staticmethod
    def encode_token(user):
        payload = {
            "sub": user.user_id,
            "exp": datetime.utcnow() + timedelta(minutes=int(config('TOKEN_VALIDITY_VALUE_IN_MINUTES')))
        }
        return jwt.encode(payload, key=config("JWT_SECRET"), algorithm="HS256")
