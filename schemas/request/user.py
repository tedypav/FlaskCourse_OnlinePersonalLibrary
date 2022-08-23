from marshmallow import fields, validate, Schema

from utils.general_validators import validate_phone_number


class UpdateUserSchemaRequest(Schema):
    first_name = fields.Str(required=False, validate=validate.Length(min=1, max=30))
    last_name = fields.Str(required=False, validate=validate.Length(min=1, max=30))
    phone = fields.Str(required=False, validate=validate_phone_number)
    company = fields.Str(required=False, validate=validate.Length(min=1, max=50))
    job_position = fields.Str(required=False, validate=validate.Length(min=1, max=50))
