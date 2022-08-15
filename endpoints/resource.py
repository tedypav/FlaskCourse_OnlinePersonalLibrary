from flask import request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from managers.auth import auth
from managers.resource import ResourceManager
from managers.tag import TagManager
from schemas.base import BaseTagSchema
from schemas.request.resource import ResourceSchemaRequest
from schemas.response.resource import ResourceSchemaResponse, FullResourceSchemaResponse
from utils.decorators import validate_schema


class ResourceRegisterResource(Resource):
    @auth.login_required
    @validate_schema(ResourceSchemaRequest)
    def post(self):
        data = request.get_json()
        owner = auth.current_user()
        new_resource = ResourceManager.register(data, owner)
        return {"resource": ResourceSchemaResponse().dump(new_resource),
                "message": "You successfully created a new resource! \N{slightly smiling face}"}, status.HTTP_201_CREATED


class ListResourceResource(Resource):
    @auth.login_required
    def get(self):
        owner = auth.current_user()
        resources = ResourceManager.get_resources(owner)
        return {"messages": "Below is a list of all resources you have previously registered \N{slightly smiling face}"
               , "resources": FullResourceSchemaResponse().dump(resources, many=True)}, status.HTTP_200_OK


class TagResourceResource(Resource):
    @auth.login_required
    @validate_schema(BaseTagSchema)
    def post(self):
        data = request.get_json()
        owner = auth.current_user()
        if not data["resource_id"] in ResourceManager.get_resources(owner)["resource_id"]:
            raise Forbidden("You do not have the necessary permissions to update this information \N{unamused face}")

        tags = TagManager.assign_tag(data)
        return {"resource": ResourceSchemaResponse().dump(tags),
                "message": "You successfully created a new resource! \N{slightly smiling face}"}, status.HTTP_201_CREATED