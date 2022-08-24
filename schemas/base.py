from decouple import config
from marshmallow import Schema, fields, validate

from utils.general_validators import validate_password


class AuthBase(Schema):
    """
    A basic schema used for the user authentication.
    """

    email = fields.Email(required=True)
    password = fields.Str(
        required=True,
        validate=validate.And(
            validate.Length(
                min=int(config("PASSWORD_MIN_LENGTH")),
                max=int(config("PASSWORD_MAX_LENGTH")),
            ),
            validate_password,
        ),
    )


class BaseResourceSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    author = fields.Str(required=True, validate=validate.Length(min=3, max=150))


class BaseTagSchema(Schema):
    tag = fields.Str(required=True, validate=validate.Length(min=1, max=50))
