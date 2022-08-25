from flask_api import status
from flask_restful import Resource

from managers.auth import auth
from managers.tag import TagManager
from schemas.response.tag import TagSchemaResponse


class ListTagsResource(Resource):
    """
    Lists all tags that the user has previously used. Validates that the user is authenticated. If everything is okay,
    returns 200 OK and a list of the tags and their IDs.

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def get(self):
        owner = auth.current_user()
        resources = TagManager.get_tags(owner)

        if len(resources) == 0:
            return {
                "message": f"You still haven't tagged anything, so you don't have any registered tags \N{slightly smiling face}"
            }
        return {
            "message": "Below is a list of all tags you have previously used \N{slightly smiling face}",
            "tags": TagSchemaResponse().dump(resources, many=True),
        }, status.HTTP_200_OK


class DeleteTagNameResource(Resource):
    """
    Deletes a tag and assignments related to it. Validates that the user is authenticated, then makes sure that they
    have previously used this tag. If everything is okay, returns 200 OK.

    Headers: "Authorization": "Bearer <token>"
    """

    @auth.login_required
    def delete(self, tag):
        owner = auth.current_user()
        TagManager.delete_tag(tag, owner.user_id)
        return {
            "message": f"You successfully deleted the tag {tag} and all assignments associated to it."
        }, status.HTTP_200_OK
