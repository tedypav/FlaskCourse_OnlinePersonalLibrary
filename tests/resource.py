import os
from unittest.mock import patch

from flask_testing import TestCase

import constants
from db import db
from config import create_app
from managers.user import UserManager
from models import UserModel, ResourceModel
from tests.base import generate_token
from tests.factories import UserFactory


class TestResourceRegister(TestCase):
    url = "/new_resource/"

    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_resource_schema_missing_fields_raises(self):
        resources = ResourceModel.query.all()
        assert len(resources) == 0

        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.post(self.url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {
            "title": ["Missing data for required field."],
            "author": ["Missing data for required field."],
        }

        users = ResourceModel.query.all()
        assert len(users) == 0

