from flask import request
from flask_api import status
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from managers.auth import auth
from managers.resource import ResourceManager
from managers.tag import TagManager
from schemas.base import BaseTagSchema
from schemas.request.resource import ResourceSchemaRequest
from schemas.request.tag import TagSchemaRequest
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
    @validate_schema(TagSchemaRequest)
    def post(self):
        data = request.get_json()
        owner = auth.current_user()
        resource_id = int(data["resource_id"])
        resource = ResourceManager.get_single_resource(resource_id)

        if not owner.user_id == int(FullResourceSchemaResponse().dump(resource)["owner_id"]):
            raise Forbidden("You need to be the owner of this resource to tag it \N{unamused face}")



        for tag in data["tag"]:
            tag_info = TagManager.register(tag, owner)
            TagManager.assign_tag(resource_id, tag_info.tag_id)
        #
        #

        # return {"message": "You successfully assigned tags to an existing resource! \N{slightly smiling face}"
        #                    , "resource": FullResourceSchemaResponse().dump(resource)}, status.HTTP_201_CREATED
        # return FullResourceSchemaResponse().dump(ResourceManager.get_resources(owner), many=True)

        return FullResourceSchemaResponse().dump(resource)