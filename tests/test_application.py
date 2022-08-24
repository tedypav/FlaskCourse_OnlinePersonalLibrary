from flask_testing import TestCase

from config import create_app
from db import db

AUTHORISED_ENDPOINTS_DATA = (
    ("POST", "/new_resource/"),
    ("POST", "/tag_resource/"),
    ("POST", "/upload_file/1/"),
    ("PUT", "/resource_status/1/read/"),
    ("PUT", "/resource_status/1/dropped/"),
    ("PUT", "/resource_status/1/to_read/"),
    ("PUT", "/update_resource/"),
    ("PUT", "/update_user/"),
    ("DELETE", "/delete_resource/1/"),
    ("DELETE", "/delete_tag/1/"),
    ("DELETE", "/delete_file/1/"),
    ("GET", "/my_user/"),
    ("GET", "/my_resources/"),
    ("GET", "/my_tags/"),
    ("GET", "/my_resources_with_tag/1/"),
)

UNAUTHORISED_ENDPOINTS_DATA = (
    ("POST", "/register/"),
    ("POST", "/login/"),
)

NO_INPUT_ENDPOINTS_DATA = (("GET", "/general_stats/"),)


class TestApp(TestCase):
    """
    Some basic tests validating that everything is okay with the user authentication.
    """

    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def iterate_endpoints(
        self,
        endpoints_data,
        status_code_method,
        expected_resp_body,
        headers=None,
        payload=None,
    ):
        """
        A simple function to iterate across endpoints. Makes it easier to test stuff.
        """
        if not headers:
            headers = {}
        if not payload:
            payload = {}

        resp = None
        for method, url in endpoints_data:
            if method == "GET":
                resp = self.client.get(url, headers=headers)
            elif method == "POST":
                resp = self.client.post(url, headers=headers)
            elif method == "PUT":
                resp = self.client.put(url, headers=headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=headers)
            status_code_method(resp)
            if not expected_resp_body == "":
                self.assertEqual(resp.json, expected_resp_body)

    def test_protected_endpoints(self):
        """
        Go through all endpoints that require authentication and make sure you can't get any information without a token.
        """
        self.iterate_endpoints(
            AUTHORISED_ENDPOINTS_DATA,
            self.assert_401,
            {
                "message": "You need a token to get access to this endpoint \N{winking face}"
            },
        )

    def test_unprotected_endpoints(self):
        """
        Go through all endpoints that don't require a token, but require input, and make sure you don't get anything
        without providing the right input.
        """
        self.iterate_endpoints(UNAUTHORISED_ENDPOINTS_DATA, self.assert_400, "")

    def test_no_input_endpoints(self):
        """
        Go through all unprotected endpoints that don't need input and make sure you get a response 200 OK.
        """
        self.iterate_endpoints(NO_INPUT_ENDPOINTS_DATA, self.assert_200, "")

    def test_expired_token_raises(self):
        """
        Go though all protected endpoints and make sure you get the right error when you use an expired token.
        """
        headers = {
            "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjM2LCJleHAiOjE2NjA4OTE1MTZ9.pbx2hPf9hi7JhHkRPsHeQIrcDKsZn9n80jNCVaPo3IA"
        }
        self.iterate_endpoints(
            AUTHORISED_ENDPOINTS_DATA,
            self.assert_401,
            {"message": "Sorry, your token has expired. Please, log in again."},
            headers,
        )

    def test_invalid_token_raises(self):
        """
        Go though all protected endpoints and make sure you get the right error when you use an invalid token.
        """
        headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGcin9n80jNCVaPo3IA"}
        self.iterate_endpoints(
            AUTHORISED_ENDPOINTS_DATA,
            self.assert_401,
            {
                "message": "Sorry, your token is invalid \N{unamused face}. Please, register or login again to obtain a valid token."
            },
            headers,
        )
