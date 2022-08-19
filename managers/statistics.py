from sqlalchemy import func, distinct

from db import db
from models import ResourceStatus, UserModel, TagModel
from models.resource import ResourceModel, resource_tag


class StatisticsManager:
    @staticmethod
    def get_users_stats():
        number_users = db.session.query(func.count(UserModel.user_id)).scalar()
        user_stats = {"number_of_users": number_users}
        return user_stats

    @staticmethod
    def get_resources_stats():
        number_resources = db.session.query(
            func.count(ResourceModel.resource_id)
        ).scalar()
        number_read_resources = (
            db.session.query(func.count(ResourceModel.resource_id))
            .filter(ResourceModel.status == ResourceStatus.read)
            .scalar()
        )
        number_dropped_resources = (
            db.session.query(func.count(ResourceModel.resource_id))
            .filter(ResourceModel.status == ResourceStatus.dropped)
            .scalar()
        )
        number_pending_resources = (
            db.session.query(func.count(ResourceModel.resource_id))
            .filter(ResourceModel.status == ResourceStatus.pending)
            .scalar()
        )
        number_tagged_resources = db.session.query(
            func.count(distinct(resource_tag.columns.resource_id))
        ).scalar()
        resource_stats = {
            "number_of_resources": number_resources,
            "number_of_read_resouces": number_read_resources,
            "number_of_dropped_resouces": number_dropped_resources,
            "number_of_pending_resouces": number_pending_resources,
            "number_of_tagged_resouces": number_tagged_resources,
        }
        return resource_stats

    @staticmethod
    def get_tags_stats():
        number_tags = db.session.query(func.count(TagModel.tag_id)).scalar()
        tag_stats = {"number_of_tags": number_tags}
        return tag_stats
