from werkzeug.exceptions import BadRequest

from db import db
from models import TagModel
from models.resource import ResourceModel, resource_tag
from schemas.response.tag import TagSchemaResponse


class TagManager:
    @staticmethod
    def get_tags(owner):
        """
        Get all tags used by the user.

        :param owner: UserModel object
        :return: tags: TagModel object, full of all tags used by the user
        """
        return TagModel.query.filter_by(owner_id=owner.user_id).all()

    @staticmethod
    def find_tag(tag, user_id):
        """
        Get tag information.

        :param tag: string, the tag that must be fetched
        :param user_id: int, the user ID
        :return: TagModel object, containing all information from the tag table about the tag
        """
        tag = TagModel.query.filter_by(tag=tag, owner_id=user_id).first()
        if tag is None:
            raise BadRequest("You haven't used this tag before \N{unamused face}")
        return tag

    @staticmethod
    def register(tag, owner):
        """
        Register a tag. Check if this user previously used the tag. If it's a new tag, register it in the database.

        :param tag: string, a tag incoming to the library
        :param owner: UserModel object
        :return: TagModel object, containing the created tag
        """
        tag_data = {"tag": tag, "owner_id": owner.user_id}

        # Check if the same tag already exists for this user
        existing_tags = TagModel.query.filter_by(
            tag=tag, owner_id=owner.user_id
        ).first()
        data = TagModel(**tag_data)

        # If the tag already exists, just return it
        if existing_tags:
            return TagModel.query.filter_by(tag=tag, owner_id=owner.user_id).first()

        # If the tag doesn't exist, create it and return it
        db.session.add(data)
        db.session.commit()
        return TagModel.query.filter_by(tag=tag, owner_id=owner.user_id).first()

    @staticmethod
    def assign_tag(resource_id, tag_id):
        """
        Assign a tag to a resource.

        :param resource_id: int, resource ID to which will be tagged
        :param tag_id: int, tag ID of the tagged that will be assigned to the resource
        :return: ResourceModel object, containing the newly-tagged resource with all its information
        """
        existing_assignment = (
            db.session.query(resource_tag)
            .filter_by(tag_id=tag_id, resource_id=resource_id)
            .count()
        )

        # If the assignment exists already, just return the resource information
        if existing_assignment > 0:
            return ResourceModel.query.filter_by(resource_id=resource_id).first()

        # Create the assignment and write it to the database
        statement = resource_tag.insert().values(tag_id=tag_id, resource_id=resource_id)
        db.session.execute(statement)
        db.session.commit()
        return ResourceModel.query.filter_by(resource_id=resource_id).first()

    @staticmethod
    def find_assignments(tag_id):
        """
        Find all resources assigned to this tag.

        :param tag_id: int, tag ID
        :return: BaseQuery object, containing the assignments this tag is used in
        """
        return db.session.query(resource_tag).filter_by(tag_id=tag_id)

    @staticmethod
    def delete_tag(tag, user_id):
        """
        Delete a tag and all assignments to it.

        :param tag: string, a tag to be deleted
        :param user_id: int, the requester (user) ID
        """
        tag = TagManager.find_tag(tag, user_id)
        tag_id = TagSchemaResponse().dump(tag)["tag_id"]

        # Delete assignments to the tag
        assignments = TagManager.find_assignments(tag_id=tag_id)
        assignments.delete(synchronize_session=False)

        # Delete the tag
        db.session.delete(tag)
        db.session.commit()
