from marshmallow import fields, Schema


class TagSchemaResponse(Schema):
    tag = fields.Str(required=True)
    tag_id = fields.Int(required=True)

class TagShortSchemaResponse(Schema):
    tag = fields.Str(required=True)
