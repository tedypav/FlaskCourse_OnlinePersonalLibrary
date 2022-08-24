from sqlalchemy import func, UniqueConstraint

from db import db


class TagModel(db.Model):
    """
    A model for the creation of the tag table.
    """

    __tablename__ = "tag"

    tag_id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.user_id"))
    created_datetime = db.Column(db.DateTime, server_default=func.now())
    updated_datetime = db.Column(db.DateTime, server_default=func.now())
    __table_args__ = (UniqueConstraint("tag", "owner_id", name="_user_tag"),)
