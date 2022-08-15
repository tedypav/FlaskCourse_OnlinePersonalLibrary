from endpoints.auth import *
from endpoints.resource import *

routes = (
    (RegisterResource, "/register/"),
    (LoginResource, "/login/"),
    (ResourceRegisterResource, "/new_resource/"),
    (ListResourceResource, "/my_resources/"),
    (TagResourceResource, "/tag_resource/"),
)
