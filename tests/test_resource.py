import os
from unittest.mock import patch

from flask_testing import TestCase

import constants
from db import db
from config import create_app
from managers.user import UserManager
from models import UserModel, ResourceModel
from tests.base import generate_token
from tests.factories import UserFactory, ResourceFactory


class TestResourceRegister(TestCase):


    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_resource_schema_missing_fields_raises(self):
        url = "/new_resource/"
        resources = ResourceModel.query.all()
        assert len(resources) == 0

        user = UserFactory()
        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        data = {}
        resp = self.client.post(url, headers=headers, json=data)
        self.assert400(resp)

        assert resp.json["message"] == {
            "title": ["Missing data for required field."],
            "author": ["Missing data for required field."],
        }

        users = ResourceModel.query.all()
        assert len(users) == 0

    def test_update_others_resource(self):
        url = "/update_resource/"
        user1 = UserFactory()
        token = generate_token(user1)
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        user2 = UserFactory()
        resource = ResourceFactory(owner_id=user2.user_id)
        data = {"resource_id": resource.resource_id}
        resp = self.client.put(url, headers=headers, json=data)
        self.assert403(resp)

        assert resp.json["message"] == "You need to be the owner of this resource to change or delete it 😒"

        url_status1 = f"/resource_status/{resource.resource_id}/read/"
        resp = self.client.put(url_status1, headers=headers, json=data)
        self.assert403(resp)

        assert resp.json["message"] == "You need to be the owner of this resource to change or delete it 😒"

        url_status2 = f"/resource_status/{resource.resource_id}/dropped/"
        resp = self.client.put(url_status2, headers=headers, json=data)
        self.assert403(resp)

        assert resp.json["message"] == "You need to be the owner of this resource to change or delete it 😒"

        url_status3 = f"/resource_status/{resource.resource_id}/to_read/"
        resp = self.client.put(url_status3, headers=headers, json=data)
        self.assert403(resp)

        assert resp.json["message"] == "You need to be the owner of this resource to change or delete it 😒"

    def test_delete_others_resource(self):
        user1 = UserFactory()
        token = generate_token(user1)
        headers = {
            "Authorization": f"Bearer {token}",
        }
        user2 = UserFactory()
        db.session.commit()
        resource = ResourceFactory(owner_id=user2.user_id)
        url = f"/delete_resource/{resource.resource_id}/"
        resp = self.client.delete(url, headers=headers)
        self.assert403(resp)

        assert resp.json["message"] == "You need to be the owner of this resource to change or delete it 😒"

    def test_get_all_resources(self):
        url = "/my_resources/"

        user = UserFactory()
        user2 = UserFactory()
        new_resource = ResourceFactory(owner_id=user.user_id)
        new_resource2 = ResourceFactory(owner_id=user2.user_id)
        new_resource3 = ResourceFactory(owner_id=user.user_id)

        token = generate_token(user)
        headers = {
            "Authorization": f"Bearer {token}",
        }
        resp = self.client.get(url, headers=headers)
        self.assert200(resp)
        for resource in resp.json["resources"]:
            assert resource["owner_id"] == user.user_id

        assert len(resp.json["resources"]) == 2

