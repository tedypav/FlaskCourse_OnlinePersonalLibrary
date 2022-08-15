from marshmallow import Schema, fields
from marshmallow_enum import EnumField

from models.enums import ResourceStatus
from schemas.base import BaseResourceSchema


class ResourceSchemaResponse(BaseResourceSchema):
    resource_id = fields.Int(required=True)
    created_datetime = fields.DateTime(required=True)
    status = EnumField(ResourceStatus, by_value=True)