from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models import UserRole
from models.user import UserModel
from managers.auth import AuthManager


class UserManager:
    @staticmethod
    def register(user_data):
        if UserModel.query.filter(UserModel.email == user_data["email"]).count() == 0:
            user_data["password"] = generate_password_hash(user_data["password"], method='sha256')
            user_data["user_role"] = UserRole.user
            user = UserModel(**user_data)
            db.session.add(user)
            db.session.commit()
            return AuthManager.encode_token(user)
        raise BadRequest("There is already an account with this e-mail. Please, log in or register with another e-mail \N{slightly smiling face}")

    @staticmethod
    def login(login_data):
        user = UserModel.query.filter_by(email=login_data["email"]).first()
        if not user:
            raise BadRequest("This e-mail hasn't been registered in the library. Please, register or check your input data \N{pensive face}")

        if check_password_hash(user.password, login_data["password"]):
            return AuthManager.encode_token(user)
        raise BadRequest("The provided password is incorrect. Please, try again \N{pensive face}")

    @staticmethod
    def get_user_info(user_id):
        user = UserModel.query.filter_by(user_id=user_id).first()
        return user

