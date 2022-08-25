from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.user import UserManager
from schemas.request.user import UpdateUserSchemaRequest
from schemas.response.user import UserSchemaResponse
from utils.decorators import validate_schema


class GetUserInfoResource(Resource):
    """
    Provides the profile information of the user-requester. It validates that the user is registered and if the token is
    valid, returns the user data.

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def get(self):
        owner = auth.current_user()
        user = UserManager.get_user_info(owner.user_id)
        return {
            "message": f"Below you'll find your user information.",
            "user": UserSchemaResponse().dump(user),
        }, status.HTTP_200_OK


class UpdateUserResource(Resource):
    """
    Updates the information of the user-requester. It validates that the provided token is valid, and that the provided
    data matches the requested format. If everything is okay, we get a happy message and 200 OK. If the provided dictionary
    is empty, we get a 400 BAD REQUEST.

    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: first_name (optional; a string between 1 and 30 characters)
          last_name (optional; a string between 1 and 30 characters)
          phone (optional; a valid phone number of the format "+[country code][phone number]")
          company (optional; a string between 1 and 50 characters)
          job_position (optional; a string between 1 and 50 characters)
    """

    @auth.login_required
    @validate_schema(UpdateUserSchemaRequest)
    def put(self):
        owner = auth.current_user()
        data = request.get_json()
        if data == {}:
            return {
                "message": f"You need to provide us with information to be updated."
            }, status.HTTP_400_BAD_REQUEST
        UserManager.update_user(owner.user_id, data)
        return {
            "message": f"You successfully updated your user information."
        }, status.HTTP_200_OK
