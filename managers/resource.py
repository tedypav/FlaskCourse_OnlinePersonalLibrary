from werkzeug.exceptions import BadRequest, Forbidden
from werkzeug.security import generate_password_hash
from flask import request
from flask_api import status
from db import db
from models import ResourceStatus
from models.resource import ResourceModel
from managers.auth import AuthManager
from schemas.response.resource import FullResourceSchemaResponse


class ResourceManager:
    @staticmethod
    def register(resource_data, owner):
        resource_data["owner_id"] = owner.user_id
        data = ResourceModel(**resource_data)
        db.session.add(data)
        db.session.flush()
        return data

    @staticmethod
    def get_resources(owner):
        return ResourceModel.query.filter_by(owner_id=owner.user_id).all()

    @staticmethod
    def get_single_resource(resource_id):
        resource = ResourceModel.query.filter_by(resource_id=resource_id).first()

        if resource is None:
            raise BadRequest("Don't try to trick up, this resource doesn't exist! \N{winking face}")

        return resource

    @staticmethod
    def authenticate_owner(resource_id, user_id):
        resource = ResourceManager.get_single_resource(resource_id)
        if not user_id == int(FullResourceSchemaResponse().dump(resource)["owner_id"]):
            raise Forbidden("You need to be the owner of this resource to tag it \N{unamused face}")
        return True

    @staticmethod
    def read(resource_id):
        ResourceModel.query.filter_by(resource_id=resource_id).update({"status": ResourceStatus.read})


    @staticmethod
    def dropped(resource_id):
        ResourceModel.query.filter_by(resource_id=resource_id).update({"status": ResourceStatus.dropped})


    @staticmethod
    def to_read(resource_id):
        ResourceModel.query.filter_by(resource_id=resource_id).update({"status": ResourceStatus.pending})
