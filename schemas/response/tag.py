from marshmallow import fields

from schemas.base import BaseTagSchema


class TagShortSchemaResponse(BaseTagSchema):
    pass


class TagSchemaResponse(BaseTagSchema):
    tag_id = fields.Int(required=True)
