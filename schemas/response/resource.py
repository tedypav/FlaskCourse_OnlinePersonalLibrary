from marshmallow import fields, validate
from marshmallow_enum import EnumField

from models.enums import ResourceStatus
from schemas.base import BaseResourceSchema
from schemas.response.tag import TagShortSchemaResponse
from utils.general_validators import validate_tag_length


class ResourceSchemaResponse(BaseResourceSchema):
    resource_id = fields.Int(required=True)
    created_datetime = fields.DateTime(required=True)
    status = EnumField(ResourceStatus, by_value=True)


class FullResourceSchemaResponse(ResourceSchemaResponse):
    link = fields.Str(required=True, validate=validate.Length(min=3, max=300))
    notes = fields.Str(required=True)
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    updated_datetime = fields.DateTime(required=True)
    owner_id = fields.Int(required=True)
    tags = fields.Nested(
        TagShortSchemaResponse, many=True, validate=validate_tag_length
    )
    file_url = fields.Str(required=True, validate=validate.Length(min=3, max=300))
