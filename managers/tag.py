from sqlalchemy.orm import load_only
from werkzeug.exceptions import BadRequest
from werkzeug.security import generate_password_hash
from flask import request
from flask_api import status
from db import db
from models import TagModel
from models.resource import ResourceModel, resource_tag
from managers.auth import AuthManager
from schemas.response.tag import TagSchemaResponse


class TagManager:

    @staticmethod
    def get_tags(owner):
        return TagModel.query.filter_by(owner_id=owner.user_id).all()

    # @staticmethod
    # def find_tag_id(tag, user_id):
    #     tag = TagModel.query.filter_by(tag=tag, owner_id=user_id).options(load_only('tag_id')).all()
    #     if tag is None:
    #         raise BadRequest("You haven't used this tag before \N{unamused face}")
    #     return tag

    @staticmethod
    def find_tag(tag, user_id):
        tag = TagModel.query.filter_by(tag=tag, owner_id=user_id).first()
        if tag is None:
            raise BadRequest("You haven't used this tag before \N{unamused face}")
        return tag

    @staticmethod
    def register(tag, owner):
        tag_data = {"tag": tag,
                    "owner_id": owner.user_id}
        existing_tags = TagModel.query.filter_by(tag=tag, owner_id=owner.user_id).first()
        data = TagModel(**tag_data)

        if existing_tags:
            return TagModel.query.filter_by(tag=tag, owner_id=owner.user_id).first()

        db.session.add(data)
        db.session.commit()
        db.session.flush()
        return TagModel.query.filter_by(tag=tag, owner_id=owner.user_id).first()

    @staticmethod
    def assign_tag(resource_id, tag_id):

        existing_assignment = db.session.query(resource_tag).filter_by(tag_id=tag_id, resource_id=resource_id).count()

        if existing_assignment > 0:
            return ResourceModel.query.filter_by(resource_id=resource_id).first()

        statement = resource_tag.insert().values(tag_id=tag_id, resource_id=resource_id)
        db.session.execute(statement)
        db.session.commit()
        return ResourceModel.query.filter_by(resource_id=resource_id).first()

    @staticmethod
    def find_assignments(tag_id):
        return db.session.query(resource_tag).filter_by(tag_id=tag_id)


    @staticmethod
    def delete_tag(tag, user_id):
        tag = TagManager.find_tag(tag, user_id)
        tag_id = TagSchemaResponse().dump(tag)["tag_id"]
        assignments = TagManager.find_assignments(tag_id = tag_id) #db.session.query(resource_tag).filter_by(tag_id=tag_id)
        assignments.delete(synchronize_session=False)
        db.session.delete(tag)
        db.session.commit()