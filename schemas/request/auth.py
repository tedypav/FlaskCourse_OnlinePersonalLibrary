from decouple import config
from marshmallow import fields, validate

from schemas.base import AuthBase
from utils.general_validators import validate_phone_number, validate_password


class RegisterSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    phone = fields.Str(required=False, validate=validate_phone_number)
    company = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    job_position = fields.Str(required=False, validate=validate.Length(min=1, max=50))
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


class LoginSchemaRequest(AuthBase):
    pass
