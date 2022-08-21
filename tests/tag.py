import os
from unittest.mock import patch

from flask_testing import TestCase

import constants
from db import db
from config import create_app
from managers.user import UserManager
from models import UserModel


class TestUser(TestCase):
    url = "/register/"

    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user_schema_missing_fields_raises(self):
        users = UserModel.query.all()
        assert len(users) == 0

        headers = {
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.post(self.url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {
            "password": ["Missing data for required field."],
            "first_name": ["Missing data for required field."],
            "email": ["Missing data for required field."],
            "last_name": ["Missing data for required field."],
        }

        users = UserModel.query.all()
        assert len(users) == 0