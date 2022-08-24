from marshmallow import fields, validate, Schema

from utils.general_validators import validate_phone_number


class UserSchemaResponse(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    phone = fields.Str(required=True, validate=validate_phone_number)
    company = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    job_position = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    user_id = fields.Int(required=True)
