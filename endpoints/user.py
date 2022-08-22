from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.user import UserManager
from schemas.request.user import UpdateUserSchemaRequest
from schemas.response.user import UserSchemaResponse
from utils.decorators import validate_schema


class GetUserInfoResource(Resource):
    @auth.login_required
    def get(self):
        owner = auth.current_user()
        user = UserManager.get_user_info(owner.user_id)
        return {
            "message": f"Below you'll find your user information.",
            "user": UserSchemaResponse().dump(user),
        }, status.HTTP_200_OK


class UpdateUserResource(Resource):
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
