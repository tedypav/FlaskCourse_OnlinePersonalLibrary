from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.resource import ResourceManager
from managers.tag import TagManager
from managers.user import UserManager
from schemas.request.resource import ResourceSchemaRequest
from schemas.request.tag import TagSchemaRequest
from schemas.response.resource import ResourceSchemaResponse, FullResourceSchemaResponse
from schemas.response.tag import TagSchemaResponse
from schemas.response.user import UserSchemaResponse
from utils.decorators import validate_schema


class GetUserInfoResource(Resource):
    @auth.login_required
    def get(self):
        owner = auth.current_user()
        user = UserManager.get_user_info(owner.user_id)

        return {"message": f"Below you'll find your user information."
                , "user": UserSchemaResponse().dump(user)}, status.HTTP_200_OK