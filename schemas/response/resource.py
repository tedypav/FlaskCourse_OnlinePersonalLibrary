from marshmallow import fields, validate
from marshmallow_enum import EnumField

from models.enums import ResourceStatus
from schemas.base import BaseResourceSchema
from schemas.response.tag import TagShortSchemaResponse


class ResourceSchemaResponse(BaseResourceSchema):
    resource_id = fields.Int(required=True)
    created_datetime = fields.DateTime(required=True)
    status = EnumField(ResourceStatus, by_value=True)


class FullResourceSchemaResponse(BaseResourceSchema):
    resource_id = fields.Int(required=True)
    status = EnumField(ResourceStatus, by_value=True)
    link = fields.Str(required=True)
    notes = fields.Str(required=True)
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=5))
    created_datetime = fields.DateTime(required=True)
    updated_datetime = fields.DateTime(required=True)
    owner_id = fields.Int(required=True)
    tags = fields.Nested(TagShortSchemaResponse, many=True)
    file_url = fields.Str(required=True)
