from endpoints.auth import *
from endpoints.resource import *

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

)
