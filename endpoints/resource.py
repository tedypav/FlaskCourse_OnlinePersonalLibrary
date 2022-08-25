from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.resource import ResourceManager
from managers.tag import TagManager
from schemas.request.resource import (
    ResourceSchemaRequest,
    UpdateResourceSchemaRequest,
)
from schemas.request.tag import TagSchemaRequest
from schemas.response.resource import ResourceSchemaResponse, FullResourceSchemaResponse
from schemas.response.tag import TagSchemaResponse
from utils.decorators import validate_schema


class ResourceRegisterResource(Resource):
    """
    A resource for resource registration. Validates that the provided data matches the requested schema.
    Validates that the user is logged in (this is a protected endpoint).
    If everything is okay, returns a happy message, 201 CREATED and basic information about the created resource.

    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: title (mandatory; a string between 3 and 150 characters)
          author (mandatory; a string between 3 and 150 characters)
          link (optional; a string between 3 and 300 characters)
          notes (optional; a text field)
          rating (optional; a number between 0 and 5, with maximum 1 number after the decimal sign)
    """

    @auth.login_required
    @validate_schema(ResourceSchemaRequest)
    def post(self):
        data = request.get_json()
        owner = auth.current_user()
        new_resource = ResourceManager.register(data, owner)
        return {
            "message": "You successfully created a new resource! \N{slightly smiling face}",
            "resource": ResourceSchemaResponse().dump(new_resource),
        }, status.HTTP_201_CREATED


class ListResourceResource(Resource):
    """
    Provides a logged in user a list of all previously registered resources.

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def get(self):
        owner = auth.current_user()
        resources = ResourceManager.get_resources(owner)

        if len(resources) == 0:
            return {
                "message": "You still haven't registered any resources \N{slightly smiling face}"
            }, status.HTTP_200_OK
        return {
            "message": "Below is a list of all resources you have previously registered \N{slightly smiling face}",
            "resources": FullResourceSchemaResponse().dump(resources, many=True),
        }, status.HTTP_200_OK


class TagResourceResource(Resource):
    """
    Tag a single resource with one or many tags (provided in the form of list of strings). Validates that the user is
    logged in and that the input data matches the requested format. Validates that the user is an owner of the provided
    resource_id.

    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: resource_id (mandatory; the ID of the resource you'd like to tag; you can check it from the
                      "Get all your resources" endpoint)
          tag (mandatory; a list of strings each of maximum length 50 characters; there is no limit
              as to how many tags you use)
    """

    @auth.login_required
    @validate_schema(TagSchemaRequest)
    def post(self):
        data = request.get_json()
        owner = auth.current_user()
        resource_id = int(data["resource_id"])

        # Get the resource information
        resource = ResourceManager.get_single_resource(resource_id)

        # Make sure the requester is the owner of the resource
        ResourceManager.authenticate_owner(resource_id, owner.user_id)

        # Go through every tag of the list, register and assign it to the resource
        for tag in data["tag"]:
            tag_info = TagManager.register(tag, owner)
            TagManager.assign_tag(resource_id, tag_info.tag_id)

        return {
            "message": "You successfully tagged the resource \N{slightly smiling face}",
            "resource": FullResourceSchemaResponse().dump(resource),
        }, status.HTTP_201_CREATED


class SetResourceReadResource(Resource):
    """
    Changes a resource status to "Read". Validates that the user is logged in, then validates that they are also the
    owner of the resource. If everything is right, we get a happy message and 200 OK.

    :param resource_id: int; the ID of the resource to be updated

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def put(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.read(resource_id)
        return {
            "message": "You successfully changed this resource's status to Read"
        }, status.HTTP_200_OK


class SetResourceDroppedResource(Resource):
    """
    Changes a resource status to "Dropped". Validates that the user is logged in, then validates that they are also the
    owner of the resource. If everything is right, we get a happy message and 200 OK.

    :param resource_id: int; the ID of the resource to be updated

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def put(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.dropped(resource_id)
        return {
            "message": "You successfully changed this resource's status to Dropped"
        }, status.HTTP_200_OK


class SetResourceToReadResource(Resource):
    """
    Changes a resource status to "To Read". Validates that the user is logged in, then validates that they are also the
    owner of the resource. If everything is right, we get a happy message and 200 OK.

    :param resource_id: int; the ID of the resource to be updated

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def put(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.to_read(resource_id)
        return {
            "message": "You successfully changed this resource's status to To Read"
        }, status.HTTP_200_OK


class DeleteResourceResource(Resource):
    """
    Deletes the resource, any files and tag assignments associated with it. Doesn't delete any tags.
    Validates that the user is logged in, then validates that they are also the owner of the resource.
    If everything is right, we get a happy message and 200 OK.

    :param resource_id: int; the ID of the resource to be updated

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def delete(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        resource = ResourceManager.get_single_resource(resource_id)

        # Check if there is a file associated with the resource and delete it, if there is
        url = FullResourceSchemaResponse().dump(resource)["file_url"]
        if url is not None:
            file_name = url.split("/")[-1]
            ResourceManager.delete_file(file_name)

        # Delete the resource and all its tag assignments
        ResourceManager.delete_resource(resource_id)
        return {
            "message": f"You successfully deleted resource with ID = {resource_id}."
        }, status.HTTP_200_OK


class GetResourceByTagResource(Resource):
    """
    Gets all resources that the user has registered and has assigned under this tag.
    Validates that the user is logged in, then validates that they are also the owner of the resource.
    Validates that the user has also previously used the tag and has assigned resources under it.
    If everything is right, we get a happy message, 200 OK and a list of resources with all information about them.

    :param tag: string; a tag provided by the user

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def get(self, tag):
        owner = auth.current_user()

        # Check if the user has previously used this tag
        tag_info = TagManager.find_tag(tag, owner.user_id)
        assigned_resources = []

        # Get all resources with this tag
        assignments = TagManager.find_assignments(
            TagSchemaResponse().dump(tag_info)["tag_id"]
        )
        if assignments is None or assignments.count() == 0:
            return {
                "message": f"You still haven't tagged anything as '{tag}' \N{slightly smiling face}"
            }

        # Fill in the list of all assigned resources
        for assignment in assignments:
            resource_id = assignment[1]
            resource_info = ResourceManager.get_single_resource(resource_id)
            assigned_resources.append(ResourceSchemaResponse().dump(resource_info))

        return {
            "message": f"Below are all resources you tagged as '{tag}'",
            "resources": assigned_resources,
        }, status.HTTP_200_OK


class UpdateResourceResource(Resource):
    """
    Updates the resource. Validates that the user is logged in, then validates that they are also the
    owner of the resource, and that the provided information matches the requested schema.
    If everything is right, we get a happy message and 200 OK.

    Headers: "Authorization": "Bearer <token>"
             "Content-Type": "application/json"
    Body: resource_id (mandatory; the ID of the resource to be updated)
          title (optional; a string between 3 and 150 characters)
          author (optional; a string between 3 and 150 characters)
          link (optional; a string between 3 and 300 characters)
          notes (optional; a text field)
          rating (optional; a number between 0 and 5, with maximum 1 number after the decimal sign)
    """

    @auth.login_required
    @validate_schema(UpdateResourceSchemaRequest)
    def put(self):
        owner = auth.current_user()
        data = request.get_json()
        resource_id = int(data["resource_id"])
        ResourceManager.authenticate_owner(resource_id, owner.user_id)
        ResourceManager.update_resource(resource_id, data)
        return {
            "message": f"You successfully updated resource with ID = {resource_id}."
        }, status.HTTP_200_OK


class UploadFileResource(Resource):
    """
    Uploads a file to a previously registered resource. Validates that the user is logged in, then validates that they are also the
    owner of the resource, and that there is a provided file. If the resourse already has a file connected to it,
    it will be overwritten. If everything is okay, we get a happy message, the URL to the file and 201 CREATED.

    Headers: "Authorization": "Bearer <token>"
    Form: file=<path to uploaded file>
    """

    @auth.login_required
    def post(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)

        # Make sure there is a file attached to the request
        try:
            file = request.files["file"]

            # Get the resource information, so we can check if it's already related to a file in the S3 bucket
            resource = ResourceManager.get_single_resource(resource_id)

            current_url = FullResourceSchemaResponse().dump(resource)["file_url"]

            # If there is a related file already, delete it forever
            if current_url is not None and current_url != "":
                file_name = current_url.split("/")[-1]
                ResourceManager.delete_file(file_name)

            # Upload the new file, then update the resource with the new link
            url = ResourceManager.upload_file(resource_id, file)
            data = {"file_url": url}
            ResourceManager.update_resource(resource_id, data)
            return {
                "message": f"You successfully uploaded the file in the following location: {url}"
            }, status.HTTP_201_CREATED

        # If there isn't a file in the request, remind the user to attach it
        except:
            return {
                "message": "You probably forgot to attach the file \N{slightly smiling face} Please, provide it in the form-data section, with key = file."
            }, status.HTTP_400_BAD_REQUEST


class DeleteFileResource(Resource):
    """
    Deletes the resource file. Validates that the user is logged in, then validates that they are also the
    owner of the resource. If everything is right, we get a happy message and 200 OK.

    :param resource_id: int; the ID of the resource to be updated

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def delete(self, resource_id):
        owner = auth.current_user()
        ResourceManager.authenticate_owner(resource_id, owner.user_id)

        # Get the link to the existing file
        resource = ResourceManager.get_single_resource(resource_id)
        url = FullResourceSchemaResponse().dump(resource)["file_url"]

        # If there is no file uploaded for this resource, tell the user that we have figured it out
        if url == "" or url is None:
            return {
                "message": "Don't try to fool us! There is no file associated with this resource \N{slightly smiling face}"
            }, status.HTTP_400_BAD_REQUEST

        # Get the pure file name, so we can use it in the delete function
        file_name = url.split("/")[-1]
        ResourceManager.delete_file(file_name)
        data = {"file_url": ""}

        # Finally, update the resource information and remove the file link
        ResourceManager.update_resource(resource_id, data)
        return {
            "message": "The file is now gone forever \N{unamused face}"
        }, status.HTTP_200_OK
