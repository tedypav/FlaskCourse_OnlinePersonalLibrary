from marshmallow import fields, Schema


class TagSchemaRequest(Schema):
    tag = fields.List(fields.String(), required=True)
    resource_id = fields.Int(required=True)
