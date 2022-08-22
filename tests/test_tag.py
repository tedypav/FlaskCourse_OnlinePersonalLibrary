import os
from unittest.mock import patch

from flask_testing import TestCase

import constants
from db import db
from config import create_app
from managers.tag import TagManager
from managers.user import UserManager
from models import UserModel
from tests.base import generate_token
from tests.factories import UserFactory, ResourceFactory, TagFactory


class TestTag(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_all_tags(self):
        tested_url = "/my_tags/"

        user1 = UserFactory()
        user2 = UserFactory()
        new_resource1 = ResourceFactory(owner_id=user1.user_id)
        new_resource12 = ResourceFactory(owner_id=user1.user_id)
        new_resource2 = ResourceFactory(owner_id=user2.user_id)

        url = "/tag_resource/"

        token1 = generate_token(user1)
        headers1 = {
            "Authorization": f"Bearer {token1}",
            "Content-Type": "application/json",
        }
        data1 = {
            "resource_id": new_resource1.resource_id,
            "tag": ["test_tag", "test", "tag", "test", "test"],
        }

        data12 = {
            "resource_id": new_resource12.resource_id,
            "tag": ["test_tag", "more_test", "more_tag", "resource"],
        }

        token2 = generate_token(user2)
        headers2 = {
            "Authorization": f"Bearer {token2}",
            "Content-Type": "application/json",
        }
        data2 = {
            "resource_id": new_resource2.resource_id,
            "tag": ["test_tag", "test", "tag", "tag", "more_tag"],
        }
        resp1 = self.client.post(url, headers=headers1, json=data1)
        assert resp1.status_code == 201

        resp12 = self.client.post(url, headers=headers1, json=data12)
        assert resp12.status_code == 201

        resp2 = self.client.post(url, headers=headers2, json=data2)
        assert resp2.status_code == 201

        tested_headers1 = {
            "Authorization": f"Bearer {token1}",
        }

        tested_headers2 = {
            "Authorization": f"Bearer {token2}",
        }

        tested_resp1 = self.client.get(tested_url, headers=tested_headers1)
        assert tested_resp1.status_code == 200
        assert len(tested_resp1.json["tags"]) == len(set(data1["tag"] + data12["tag"]))
        for tag in tested_resp1.json["tags"]:
            assert tag["tag"] in set(data1["tag"] + data12["tag"])

        tested_resp2 = self.client.get(tested_url, headers=tested_headers2)
        assert tested_resp2.status_code == 200
        assert len(tested_resp2.json["tags"]) == len(set(data2["tag"]))
        for tag in tested_resp2.json["tags"]:
            assert tag["tag"] in set(data2["tag"])

    def test_delete_tags(self):

        user1 = UserFactory()
        user2 = UserFactory()
        new_resource1 = ResourceFactory(owner_id=user1.user_id)
        new_resource12 = ResourceFactory(owner_id=user1.user_id)
        new_resource2 = ResourceFactory(owner_id=user2.user_id)

        tag1 = "test_tag"

        url = "/tag_resource/"

        token1 = generate_token(user1)
        headers1 = {
            "Authorization": f"Bearer {token1}",
            "Content-Type": "application/json",
        }
        data1 = {
            "resource_id": new_resource1.resource_id,
            "tag": [tag1, "test", "tag", "test", "test"],
        }

        data12 = {
            "resource_id": new_resource12.resource_id,
            "tag": [tag1, "more_test", "more_tag", "resource"],
        }

        token2 = generate_token(user2)
        headers2 = {
            "Authorization": f"Bearer {token2}",
            "Content-Type": "application/json",
        }
        data2 = {
            "resource_id": new_resource2.resource_id,
            "tag": ["test_tag", "test", "tag", "tag", "more_tag"],
        }
        resp1 = self.client.post(url, headers=headers1, json=data1)
        assert resp1.status_code == 201

        resp12 = self.client.post(url, headers=headers1, json=data12)
        assert resp12.status_code == 201

        resp2 = self.client.post(url, headers=headers2, json=data2)
        assert resp2.status_code == 201

        tested_headers1 = {
            "Authorization": f"Bearer {token1}",
        }

        user1_num_tags = len(TagManager.get_tags(user1))
        user2_num_tags = len(TagManager.get_tags(user2))
        tested_resp1 = self.client.delete(
            f"/delete_tag/{tag1}/", headers=tested_headers1
        )
        assert tested_resp1.status_code == 200
        assert (
            tested_resp1.json["message"]
            == f"You successfully deleted the tag {tag1} and all assignments associated to it."
        )
        user1_num_tags_after_delete = len(TagManager.get_tags(user1))
        user2_num_tags_after_delete = len(TagManager.get_tags(user2))
        assert user1_num_tags - 1 == user1_num_tags_after_delete
        assert user2_num_tags == user2_num_tags_after_delete
