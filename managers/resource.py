import os
import uuid

from werkzeug.utils import secure_filename

from constants import TEMP_FILE_FOLDER
from services.aws_s3_bucket import S3Service
from sqlalchemy import func
from werkzeug.exceptions import BadRequest, Forbidden

from db import db
from models import ResourceStatus
from models.resource import ResourceModel, resource_tag
from schemas.response.resource import FullResourceSchemaResponse
from utils.helpers import delete_local_file

s3 = S3Service()


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
            raise BadRequest(
                "Don't try to trick us, this resource doesn't exist! \N{winking face}"
            )

        return resource

    @staticmethod
    def authenticate_owner(resource_id, user_id):
        resource = ResourceManager.get_single_resource(resource_id)
        if not user_id == int(FullResourceSchemaResponse().dump(resource)["owner_id"]):
            raise Forbidden(
                "You need to be the owner of this resource to change or delete it \N{unamused face}"
            )
        return True

    @staticmethod
    def read(resource_id):
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"status": ResourceStatus.read}
        )
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )

    @staticmethod
    def dropped(resource_id):
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"status": ResourceStatus.dropped}
        )
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )

    @staticmethod
    def to_read(resource_id):
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"status": ResourceStatus.pending}
        )
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )

    @staticmethod
    def find_assignments(resource_id):
        return db.session.query(resource_tag).filter_by(resource_id=resource_id)

    @staticmethod
    def delete_resource(resource_id):
        resource = ResourceManager.get_single_resource(resource_id)
        assignments = ResourceManager.find_assignments(resource_id)
        assignments.delete(synchronize_session=False)
        db.session.delete(resource)
        db.session.commit()

    @staticmethod
    def update_resource(resource_id, data):
        for key, value in data.items():
            resource = ResourceModel.query.filter_by(resource_id=resource_id).update(
                {key: value}
            )

        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )
        db.session.commit()

    @staticmethod
    def upload_file(resource_id, file):
        extension = file.filename.split('.')[1]
        name = f"{str(uuid.uuid4())}.{extension}"
        file.save(os.path.join(TEMP_FILE_FOLDER, f"{name}"))
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}")
        url = s3.upload_file(path, name)
        delete_local_file(name)
        return url
