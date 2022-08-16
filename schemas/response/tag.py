from marshmallow import fields

from schemas.base import BaseTagSchema


class TagSchemaResponse(BaseTagSchema):
    tag = fields.Str(required=True)
