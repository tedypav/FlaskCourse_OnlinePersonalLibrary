from marshmallow import fields

from schemas.base import BaseTagSchema


class TagSchemaRequest(BaseTagSchema):
    tag = fields.List(fields.String(), required=True)
