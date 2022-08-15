from werkzeug.security import generate_password_hash
from flask import request
from flask_api import status
from db import db
from models import TagModel
from models.resource import ResourceModel, resource_tag
from managers.auth import AuthManager


class TagManager:
    @staticmethod
    def register(tag_data, owner):
        tag_data["owner_id"] = owner.user_id
        data = TagModel(**tag_data)
        db.session.add(data)
        db.session.flush()
        return data

    # @staticmethod
    # def get_resources(owner):
    #     return ResourceModel.query.filter_by(owner_id=owner.user_id).all()

    @staticmethod
    def assign_tag(data):
        statement = resource_tag.insert().values(tag_id=data["tag_id"], resource_id=data["resource_id"])
        db.session.execute(statement)
        db.session.commit()
        return ResourceModel.query.filter_by(resource_id=data["resource_id"]).all()
