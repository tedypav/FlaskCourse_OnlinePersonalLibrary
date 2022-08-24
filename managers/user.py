from sqlalchemy import func
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from managers.auth import AuthManager
from models import UserRole
from models.user import UserModel


class UserManager:
    @staticmethod
    def register(user_data):
        """
        Registers the user to the database.

        :param user_data: dict, data provided by the user (mandatory: "first_name", "last_name", "email" and "password")
        :return: token: string, if everything is okay; otherwise returns BadRequest
        """
        if UserModel.query.filter(UserModel.email == user_data["email"]).count() == 0:

            # Hash the password, so we don't save it in raw format in the database
            user_data["password"] = generate_password_hash(
                user_data["password"], method="sha256"
            )

            # Set user role = user (this will be different for the admin registration, when we get there)
            user_data["user_role"] = UserRole.user

            # Unpack the data and
            user = UserModel(**user_data)
            db.session.add(user)
            db.session.commit()
            return AuthManager.encode_token(user)
        raise BadRequest(
            "There is already an account with this e-mail. Please, log in or register with another e-mail \N{slightly smiling face}"
        )

    @staticmethod
    def login(login_data):
        """
        Confirms that the user was previously registered to the library. Checks that the password provided is correct.

        :param login_data:dict, e-mail and password provided by the user
        :return: If everything is okay, doesn't return anything, otherwise it returns BadRequest
        """
        user = UserModel.query.filter_by(email=login_data["email"]).first()
        if not user:
            raise BadRequest(
                "This e-mail hasn't been registered in the library. Please, register or check your input data \N{pensive face}"
            )

        if check_password_hash(user.password, login_data["password"]):
            return AuthManager.encode_token(user)
        raise BadRequest(
            "The provided password is incorrect. Please, try again \N{pensive face}"
        )

    @staticmethod
    def get_user_info(user_id):
        """
        Get all user information from the database, table user.

        :param user_id: int, ID of the requester
        :return: user: the record of the table corresponding to the user_id
        """
        user = UserModel.query.filter_by(user_id=user_id).first()
        return user

    @staticmethod
    def update_user(user_id, data):
        """
        Update the user with provided data. Write the changes in the database.

        :param user_id: int, the ID of the user
        :param data: dict, a dictionary of characteristics to be changed and their new values
        """
        for key, value in data.items():
            resource = UserModel.query.filter_by(user_id=user_id).update({key: value})

        UserModel.query.filter_by(user_id=user_id).update(
            {"updated_datetime": func.now()}
        )
        db.session.commit()
