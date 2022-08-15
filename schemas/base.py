from decouple import config
from marshmallow import Schema, fields, validate


class AuthBase(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
