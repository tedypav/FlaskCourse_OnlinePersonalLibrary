from endpoints.auth import *
from endpoints.resource import *
from endpoints.tag import *

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (ResourceRegisterResource, "/new_resource/"),
    (ListResourceResource, "/my_resources/"),
    (TagResourceResource, "/tag_resource/"),
    (SetResourceReadResource, "/resource_status/<int:resource_id>/read/"),
    (SetResourceDroppedResource, "/resource_status/<int:resource_id>/dropped/"),
    (SetResourceToReadResource, "/resource_status/<int:resource_id>/to_read/"),
    # (RegisterAdminResource, "/resource_status/register/"),
    (DeleteResourceResource, "/delete_resource/<int:resource_id>/"),
    (ListTagsResource, "/my_tags/"),
    (DeleteTagNameResource, "/delete_tag/<string:tag>/"),
    (GetResourceByTagResource, "/my_resources_with_tag/<string:tag>/"),
    (UpdateResourceResource, "/update_resource/"),

)
