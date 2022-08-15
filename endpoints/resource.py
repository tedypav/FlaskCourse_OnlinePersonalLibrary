from flask import request
from flask_api import status
from flask_restful import Resource
from decouple import config

from managers.auth import auth
from managers.resource import ResourceManager
from schemas.request.auth import LoginSchemaRequest, RegisterSchemaRequest
from schemas.request.resource import ResourceSchemaRequest
from schemas.response.resource import ResourceSchemaResponse
from utils.decorators import validate_schema, validate_password, validate_phone_number


class ResourceRegisterResource(Resource):
    # @auth.login_required
    # def get(self):
    #     user = auth.current_user()
    #     complains = ComplaintManager.get_complaints(user)
    #     return ComplaintSchemaResponse().dump(complains, many=True)

    @auth.login_required
    @validate_schema(ResourceSchemaRequest)
    def post(self):
        data = request.get_json()
        owner = auth.current_user()
        new_resource = ResourceManager.register(data, owner)
        return {"resource": ResourceSchemaResponse().dump(new_resource),
                "message": "You successfully created a new resource! \N{slightly smiling face}"}, status.HTTP_201_CREATED