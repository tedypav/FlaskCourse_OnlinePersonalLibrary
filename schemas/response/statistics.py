from marshmallow import fields, Schema


class UsersStatsResponse(Schema):
    number_users = fields.Int(required=True)


class ResourceStatsResponse(Schema):
    pending = fields.Int(required=False)
    read = fields.Int(required=False)
    to_read = fields.Int(required=False)
