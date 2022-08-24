from marshmallow import fields, Schema

from utils.general_validators import validate_tag_length


class TagSchemaRequest(Schema):
    tag = fields.List(fields.String(), required=True, validate=validate_tag_length)
    resource_id = fields.Int(required=True)
