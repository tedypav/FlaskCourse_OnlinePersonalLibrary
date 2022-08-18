from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField

from models.enums import ResourceStatus
from schemas.base import BaseResourceSchema
from schemas.response.tag import TagSchemaResponse


class ResourceSchemaResponse(BaseResourceSchema):
    resource_id = fields.Int(required=True)
    created_datetime = fields.DateTime(required=True)
    status = EnumField(ResourceStatus, by_value=True)


class FullResourceSchemaResponse(BaseResourceSchema):
    resource_id = fields.Int(required=True)
    status = EnumField(ResourceStatus, by_value=True)
    link = fields.Str(required=False)
    notes = fields.Str(required=False)
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=5))
    created_datetime = fields.DateTime(required=True)
    updated_datetime = fields.DateTime(required=True)
    owner_id = fields.Int(required=True)
    tags = fields.Nested(TagSchemaResponse, many=True)