from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.resource import ResourceManager
from managers.tag import TagManager
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
        ResourceManager.authenticate_owner(resource_id, owner.user_id)

        for tag in data["tag"]:
            tag_info = TagManager.register(tag, owner)
            TagManager.assign_tag(resource_id, tag_info.tag_id)

        return {"messages": "You successfully tagged the resource \N{slightly smiling face}"
                   , "resources": FullResourceSchemaResponse().dump(resource)}, status.HTTP_201_CREATED


class SetResourceReadResource(Resource):
    @auth.login_required
    def put(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.read(resource_id)
        return {"message": "You successfully changed this resource\'s status to Read"}, status.HTTP_200_OK


class SetResourceDroppedResource(Resource):
    @auth.login_required
    def put(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.dropped(resource_id)
        return {"message": "You successfully changed this resource\'s status to Dropped"}, status.HTTP_200_OK


class SetResourceToReadResource(Resource):
    @auth.login_required
    def put(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.to_read(resource_id)
        return {"message": "You successfully changed this resource\'s status to To Read"}, status.HTTP_200_OK


class DeleteResourceResource(Resource):
    @auth.login_required
    def delete(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.delete_resource(resource_id)
        return {"message": f"You successfully deleted resource with ID = {resource_id}."}, status.HTTP_200_OK