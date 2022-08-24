from marshmallow import fields, validate

from schemas.base import AuthBase
from utils.general_validators import validate_phone_number


class RegisterSchemaRequest(AuthBase):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    phone = fields.Str(required=False, validate=validate_phone_number)
    company = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    job_position = fields.Str(required=False, validate=validate.Length(min=1, max=50))


class LoginSchemaRequest(AuthBase):
    pass
