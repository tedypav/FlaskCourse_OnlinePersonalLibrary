from werkzeug.security import generate_password_hash

from db import db
from models.resource import ResourceModel
from managers.auth import AuthManager


class ResourceManager:
    @staticmethod
    def register(resource_data):
        resource = ResourceModel(**resource_data)
        db.session.add(resource)
        return 201
