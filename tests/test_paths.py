from flask_testing import TestCase

from config import create_app
from db import db
from models import ResourceModel


class TestApp(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_happy_path(self):

        # Register a new user
        headers = {
            "Content-Type": "application/json",
        }
        data = {
            "password": "Aa@123!53",
            "first_name": "Sarah",
            "last_name": "Brown",
            "email": "testemail@example.com",
        }
        register_resp = self.client.post("/register/", headers=headers, json=data)
        assert register_resp.status_code == 201
        assert (
            register_resp.json["message"]
            == "Welcome to our library! This token will only be valid for the next 120 minutes. After that you'll need to log in 😉"
        )

        token = register_resp.json["token"]

        # Get the new user's information

        headers = {
            "Authorization": f"Bearer {token}",
        }

        user_info_resp = self.client.get("/my_user/", headers=headers)
        assert user_info_resp.status_code == 200
        assert (
            user_info_resp.json["message"] == "Below you'll find your user information."
        )
        for key, value in user_info_resp.json["user"].items():
            if key in data:
                assert value == data[key]

        # Update the user's information

        new_data = {"company": "Test Corporation", "job_position": "QA"}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        user_update_resp = self.client.put(
            "/update_user/", headers=headers, json=new_data
        )
        assert user_update_resp.status_code == 200
        assert (
            user_update_resp.json["message"]
            == "You successfully updated your user information."
        )

        # Check updated data

        headers = {
            "Authorization": f"Bearer {token}",
        }

        user_info_resp = self.client.get("/my_user/", headers=headers)
        assert user_info_resp.status_code == 200
        assert (
            user_info_resp.json["message"] == "Below you'll find your user information."
        )
        for key, value in user_info_resp.json["user"].items():
            if key in data:
                assert value == data[key]

        # Register a new source

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        resource_data = {"title": "Test Book", "author": "Test Author"}

        register_resource_resp = self.client.post(
            "/new_resource/", headers=headers, json=resource_data
        )

        assert register_resource_resp.status_code == 201
        assert (
            register_resource_resp.json["message"]
            == "You successfully created a new resource! 🙂"
        )

        for key, value in register_resource_resp.json["resource"].items():
            if key in resource_data:
                assert value == resource_data[key]

        # Update the resource

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        resource_id = register_resource_resp.json["resource"]["resource_id"]
        update_resource_data = {
            "resource_id": resource_id,
            "title": "Test Book 2",
            "author": "Test Author, Second Author",
            "notes": "We want to test the update feature of the resources.",
        }

        update_resource_resp = self.client.put(
            "/update_resource/", headers=headers, json=update_resource_data
        )

        assert update_resource_resp.status_code == 200
        assert (
            update_resource_resp.json["message"]
            == f"You successfully updated resource with ID = {resource_id}."
        )

        # for key, value in register_resource_resp.json["resource"].items():
        #     if key in resource_data:
        #         assert value == resource_data[key]

        # Tag a resource

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        tag_data = {
            "resource_id": register_resource_resp.json["resource"]["resource_id"],
            "tag": ["test", "testing", "integration", "endpoints", "tests"],
        }

        tag_resource_resp = self.client.post(
            "/tag_resource/", headers=headers, json=tag_data
        )

        assert tag_resource_resp.status_code == 201
        assert (
            tag_resource_resp.json["message"]
            == "You successfully tagged the resource 🙂"
        )

        for tag in tag_resource_resp.json["resource"]["tags"]:
            assert tag["tag"] in set(tag_data["tag"])

        assert len(tag_resource_resp.json["resource"]["tags"]) == len(
            set(tag_data["tag"])
        )

        # Get all registered resources

        headers = {
            "Authorization": f"Bearer {token}",
        }

        get_resources_resp = self.client.get("/my_resources/", headers=headers)

        assert get_resources_resp.status_code == 200
        assert (
            get_resources_resp.json["message"]
            == "Below is a list of all resources you have previously registered 🙂"
        )

        assert (
            len(get_resources_resp.json["resources"])
            == ResourceModel.query.filter_by(
                owner_id=int(user_info_resp.json["user"]["user_id"])
            ).count()
        )

        # Login

        headers = {
            "Content-Type": "application/json",
        }

        login_data = data = {
            "password": "Aa@123!53",
            "email": "testemail@example.com",
        }

        login_resp = self.client.post("/login/", headers=headers, json=data)

        assert login_resp.status_code == 200
        assert (
            login_resp.json["message"]
            == "This token will only be valid for the next 120 minutes. After that you'll need to log in again 😉"
        )

        login_token = login_resp.json["token"]

        # Get general statistics

        stats = self.client.get("/general_stats/")

        # Get all tags

        headers = {
            "Authorization": f"Bearer {login_token}",
        }

        get_tags_resp = self.client.get("/my_tags/", headers=headers)

        assert get_tags_resp.status_code == 200
        assert (
            get_tags_resp.json["message"]
            == "Below is a list of all tags you have previously used 🙂"
        )

        assert len(get_tags_resp.json["tags"]) == len(set(tag_data["tag"]))

        # Delete the tag "test"

        headers = {
            "Authorization": f"Bearer {login_token}",
        }

        delete_tag_resp = self.client.delete("/delete_tag/test/", headers=headers)

        assert delete_tag_resp.status_code == 200
        assert (
            delete_tag_resp.json["message"]
            == "You successfully deleted the tag test and all assignments associated to it."
        )

        # Get all tags again

        headers = {
            "Authorization": f"Bearer {login_token}",
        }

        get_updated_tags_resp = self.client.get("/my_tags/", headers=headers)

        assert get_updated_tags_resp.status_code == 200
        assert (
            get_updated_tags_resp.json["message"]
            == "Below is a list of all tags you have previously used 🙂"
        )

        assert len(get_updated_tags_resp.json["tags"]) == len(set(tag_data["tag"])) - 1

        # Get all resources again

        headers = {
            "Authorization": f"Bearer {login_token}",
        }

        get_updated_resources_resp = self.client.get("/my_resources/", headers=headers)

        assert get_updated_resources_resp.status_code == 200
        assert (
            get_updated_resources_resp.json["message"]
            == "Below is a list of all resources you have previously registered 🙂"
        )

        for resource in get_updated_resources_resp.json["resources"]:
            for tag in resource["tags"]:
                assert tag["tag"] != "test"
