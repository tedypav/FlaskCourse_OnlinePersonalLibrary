from flask import request
from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.resource import ResourceManager
from managers.tag import TagManager
from schemas.request.resource import ResourceSchemaRequest
from schemas.request.tag import TagSchemaRequest
from schemas.response.resource import ResourceSchemaResponse, FullResourceSchemaResponse
from schemas.response.tag import TagSchemaResponse
from utils.decorators import validate_schema


class ListTagsResource(Resource):
    @auth.login_required
    def get(self):
        owner = auth.current_user()
        resources = TagManager.get_tags(owner)
        return {"messages": "Below is a list of all tags you have previously used \N{slightly smiling face}"
                   , "resources": TagSchemaResponse().dump(resources, many=True)}, status.HTTP_200_OK


class DeleteTagNameResource(Resource):
    @auth.login_required
    def delete(self, tag):
        owner = auth.current_user()
        TagManager.delete_tag(tag, owner.user_id)
        return {"message": f"You successfully deleted the tag {tag} and all assignments associated to it."}\
            , status.HTTP_200_OK