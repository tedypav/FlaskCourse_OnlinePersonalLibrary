import os
import uuid

from sqlalchemy import func
from werkzeug.exceptions import BadRequest, Forbidden

from constants import TEMP_FILE_FOLDER
from db import db
from models import ResourceStatus
from models.resource import ResourceModel, resource_tag
from schemas.response.resource import FullResourceSchemaResponse
from services.aws_s3_bucket import S3Service
from utils.helpers import delete_local_file

s3 = S3Service()


class ResourceManager:
    @staticmethod
    def register(resource_data, owner):
        """
        Registers a resource in the database.

        :param resource_data: dict, a dictionary with resource information (mandatory: "title", "author")
        :param owner: UserModel object, containing all information about the user
        :return: data: ResourceModel object, containing the information provided by the user
        """
        resource_data["owner_id"] = owner.user_id
        data = ResourceModel(**resource_data)
        db.session.add(data)
        db.session.commit()
        return data

    @staticmethod
    def get_resources(owner):
        """
        Returns all resources a user has registered.

        :param owner: UserModel object
        :return: ResourceModel object, containing all resources registered by the user
        """
        return ResourceModel.query.filter_by(owner_id=owner.user_id).all()

    @staticmethod
    def get_single_resource(resource_id):
        """
        Get all available information about a resource.

        :param resource_id: int, resource ID
        :return: ResourceModel object, containing all available data about the resource
        """
        resource = ResourceModel.query.filter_by(resource_id=resource_id).first()

        # If the resource doesn't exist, tell the user to think again
        if resource is None:
            raise BadRequest(
                "Don't try to trick us, this resource doesn't exist! \N{winking face}"
            )

        return resource

    @staticmethod
    def authenticate_owner(resource_id, user_id):
        """
        Make sure that the resource belongs to the provided user_id.

        :param resource_id: int, the ID of the resource in question
        :param user_id: int, the ID of the user we're checking
        :return: True: bool; if the resource doesn't belong to the user, the response is Forbidden
        """
        resource = ResourceManager.get_single_resource(resource_id)
        if not user_id == int(FullResourceSchemaResponse().dump(resource)["owner_id"]):
            raise Forbidden(
                "You need to be the owner of this resource to change or delete it \N{unamused face}"
            )
        return True

    @staticmethod
    def read(resource_id):
        """
        Change the resource status to "Read".

        :param resource_id: int, the ID of the resource that will get updated
        """
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"status": ResourceStatus.read}
        )
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )

    @staticmethod
    def dropped(resource_id):
        """
        Change the resource status to "Dropped".

        :param resource_id: int, the ID of the resource that will get updated
        """
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"status": ResourceStatus.dropped}
        )
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )

    @staticmethod
    def to_read(resource_id):
        """
        Change the resource status to "To Read".

        :param resource_id: int, the ID of the resource that will get updated
        """
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"status": ResourceStatus.pending}
        )
        ResourceModel.query.filter_by(resource_id=resource_id).update(
            {"updated_datetime": func.now()}
        )

    @staticmethod
    def find_assignments(resource_id):
        """
        Find all tags assigned to a resource.

        :param resource_id: int, the ID of the resource
        :return: BaseQuery object, containing all information about the resource assignments - resource ID, tag IDs
        """
        return db.session.query(resource_tag).filter_by(resource_id=resource_id)

    @staticmethod
    def delete_resource(resource_id):
        """
        Delete a resource and all assignments to it.

        :param resource_id: int, the ID of the resource that will get deleted
        :return: If everything is okay - nothing, otherwise - errors
        """
        try:
            resource = ResourceManager.get_single_resource(resource_id)
            assignments = ResourceManager.find_assignments(resource_id)

            # Delete assignments
            assignments.delete(synchronize_session=True)

            # Delete the resource
            db.session.delete(resource)
            db.session.commit()
        except Exception as ex:
            return ex

    @staticmethod
    def update_resource(resource_id, data):
        """
        Update a resource.

        :param resource_id: int, the ID of the resource that will get updated
        :param data: dict, a dictionary of the characteristics that need to be changed with the new values
        """
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
        """
        Upload a file to the AWS S3 Bucket and put the URL in the resource information.

        :param resource_id: int, ID of the resource to which the file will be uploaded
        :param file: file
        :return: url: string, the link to the file location in the bucket
        """

        # Get the file extension
        extension = file.filename.split(".")[1]

        # Change the file name
        name = f"{str(uuid.uuid4())}.{extension}"

        # Save the file to the temporary folder
        file.save(os.path.join(TEMP_FILE_FOLDER, f"{name}"))
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}")

        # Upload the file to the AWS S3 bucket
        url = s3.upload_file(path, name)

        # Delete the file from the local temp folder
        delete_local_file(name)
        return url

    @staticmethod
    def delete_file(file_name):
        """
        Delete a previously uploaded file.

        :param file_name: string, the name of the file to be deleted
        :return: Nothing, if everything is okay; otherwise return errors
        """
        try:
            s3.delete_file(file_name)
        except Exception as ex:
            return ex
