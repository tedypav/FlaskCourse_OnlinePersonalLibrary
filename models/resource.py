from sqlalchemy import func

from db import db
from models.enums import ResourceStatus


class ResourceModel(db.Model):
    __tablename__ = "resource"

    resource_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    link = db.Column(db.String(300), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Numeric(1, 1), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    status = db.Column(
        db.Enum(ResourceStatus),
        default=ResourceStatus.pending,
        nullable=False
    )
    created_datetime = db.Column(db.DateTime, server_default=func.now())
    updated_datetime = db.Column(db.DateTime, server_default=func.now())


resource_tag = db.Table(
    "resource_tag",
    db.Model.metadata,
    db.Column("resource_tag_id", db.Integer, primary_key=True),
    db.Column("resource_id", db.Integer, db.ForeignKey("resource.resource_id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.tag_id")),
)