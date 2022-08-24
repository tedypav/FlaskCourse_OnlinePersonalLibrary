"""test change in resourc emodel

Revision ID: 59fb7b8bff11
Revises: ee590c396f2f
Create Date: 2022-08-15 20:51:20.545331

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "59fb7b8bff11"
down_revision = "ee590c396f2f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "resource",
        sa.Column("resource_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("author", sa.String(length=150), nullable=False),
        sa.Column("link", sa.String(length=300), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("rating", sa.Numeric(precision=2, scale=1), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("read", "pending", "dropped", name="resourcestatus"),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "created_datetime",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "updated_datetime",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["user.user_id"],
        ),
        sa.PrimaryKeyConstraint("resource_id"),
    )
    op.create_foreign_key(
        None, "resource_tag", "resource", ["resource_id"], ["resource_id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "resource_tag", type_="foreignkey")
    op.drop_table("resource")
    # ### end Alembic commands ###
