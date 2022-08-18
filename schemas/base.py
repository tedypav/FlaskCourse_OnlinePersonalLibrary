from marshmallow import Schema, fields, validate


class AuthBase(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class BaseResourceSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=3, max=150))
    author = fields.Str(required=True, validate=validate.Length(min=3, max=150))



