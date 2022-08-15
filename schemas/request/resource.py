from marshmallow import fields, validate
from schemas.base import BaseResourceSchema


class ResourceSchemaRequest(BaseResourceSchema):
    link = fields.Str(required=False, validate=validate.Length(min=3, max=300))
    notes = fields.Str(required=False)
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=5))

