from marshmallow import fields, validate, Schema

from schemas.base import BaseResourceSchema


class ResourceSchemaRequest(BaseResourceSchema):
    link = fields.Str(required=False, validate=validate.Length(min=3, max=300))
    notes = fields.Str(required=False)
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=5))


class UpdateResourceSchemaRequest(Schema):
    resource_id = fields.Int(required=True)
    title = fields.Str(required=False, validate=validate.Length(min=3, max=150))
    author = fields.Str(required=False, validate=validate.Length(min=3, max=150))
    link = fields.Str(required=False)
    notes = fields.Str(required=False)
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=5))


class UploadFileResourceSchemaRequest(Schema):
    file = fields.Raw(required=True, type='file')
