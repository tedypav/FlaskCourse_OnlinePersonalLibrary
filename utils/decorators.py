from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    """
    Validate that the provided data matches the requested schema.

    :param schema_name: schema
    :return If everything is okay, func(*args, **kwargs): the function that is modified by the decorator
            If there is an error - BadRequest with a long list of errors
    """

    def decorated_function(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)

        return wrapper

    return decorated_function


def permission_required(role):
    """
    Validate that the user has the necessary role to perform an action.

    :param role: string; the necessary role to perform an action
    :return If everything is okay, func(*args, **kwargs): the function that is modified by the decorator
            If there is an error - Forbidden with a sad message about the user's permission level

    """

    def decorated_function(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if not current_user.role == role:
                raise Forbidden(
                    "You do not have the necessary permissions to access this information \N{unamused face}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorated_function
