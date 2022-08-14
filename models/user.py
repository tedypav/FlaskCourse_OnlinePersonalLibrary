from sqlalchemy import func

from db import db


class UserModel(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(50), nullable=True)
    job_position = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    # tags = db.relationship("TagModel", backref="tag", lazy='dynamic')
    # resources = db.relationship("ResourceModel", backref="resource", lazy='dynamic')
    created_datetime = db.Column(db.DateTime, server_default=func.now())
    updated_datetime = db.Column(db.DateTime, server_default=func.now())
