from werkzeug.security import generate_password_hash
from flask import request
from flask_api import status
from db import db
from models.resource import ResourceModel
from managers.auth import AuthManager


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
