from flask_testing import TestCase

from config import create_app
from db import db
from models import UserModel
from schemas.response.user import UserSchemaResponse
from tests.base import generate_token
from tests.factories import UserFactory


class TestUser(TestCase):
    """
    A class to test user operations.
    """
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user_schema_missing_fields_raises(self):
        """
        Make sure that a user can't register if they don't provide all necessary information.
        """
        url = "/register/"
        users = UserModel.query.all()
        assert len(users) == 0

        headers = {
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {
            "password": ["Missing data for required field."],
            "first_name": ["Missing data for required field."],
            "email": ["Missing data for required field."],
            "last_name": ["Missing data for required field."],
        }

        users = UserModel.query.all()
        assert len(users) == 0

    def test_login_no_credentials(self):
        """
        Make sure a user can't login, if they haven't provided any credentials.
        """
        url = "/login/"
        headers = {
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {
            "email": ["Missing data for required field."],
            "password": ["Missing data for required field."],
        }

    def test_login_unregistered_email(self):
        """
        Make sure a user can't login, if they provide an unregistered e-mail.
        """
        url = "/login/"
        headers = {
            "Content-Type": "application/json",
        }
        data = {"email": "unregistered@email.com", "password": "Somepass1@"}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)

        assert (
            resp.json["message"]
            == "This e-mail hasn't been registered in the library. Please, register or check your input data 😔"
        )

    def test_login_invalid_email(self):
        """
        Make sure the users can't login if they provide an invalid e-mail address.
        """
        url = "/login/"
        headers = {
            "Content-Type": "application/json",
        }
        data = {"email": "invalidemail", "password": "Somepass1@"}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {"email": ["Not a valid email address."]}

    def test_login_incorrect_pass(self):
        """
        Make sure that users can't login if they provide an incorrect password.
        """
        url = "/login/"

        user = UserFactory()

        headers = {
            "Content-Type": "application/json",
        }
        data = {"email": user.email, "password": "Somepass1@"}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)

        assert (
            resp.json["message"]
            == "The provided password is incorrect. Please, try again 😔"
        )

    def test_get_own_user_info(self):
        """
        Make sure that the users will only get their own information when requested.
        Make sure they get the right data.
        """
        url = "/my_user/"

        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
        }
        resp = self.client.get(url, headers=headers)
        self.assert200(resp)

        assert resp.json["user"]["user_id"] == user.user_id

    def test_update_own_info(self):
        """
        Make sure the users can only update their own information, and that the update works.
        """
        url = "/update_user/"

        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {
            "first_name": "Test",
            "last_name": "Testov",
            "company": "Random Comp",
            "job_position": "Tester",
        }
        resp = self.client.put(url, headers=headers, json=data)
        self.assert200(resp)

        assert resp.json["message"] == "You successfully updated your user information."

        new_user = UserModel.query.filter_by(user_id=user.user_id).first()
        new_user_info = UserSchemaResponse().dump(new_user)
        assert new_user_info["first_name"] == data["first_name"]
        assert new_user_info["last_name"] == data["last_name"]
        assert new_user_info["company"] == data["company"]
        assert new_user_info["job_position"] == data["job_position"]

    def test_update_without_info(self):
        """
        Make sure the users can't update their profile without providing correct information.
        """
        url = "/update_user/"

        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.put(url, headers=headers, json=data)
        self.assert400(resp)

        assert (
            resp.json["message"]
            == "You need to provide us with information to be updated."
        )
