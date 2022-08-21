"""Adding unique field

Revision ID: b7be7512263d
Revises: b50bdadac915
Create Date: 2022-08-14 19:31:49.923379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b7be7512263d"
down_revision = "b50bdadac915"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "user", ["email"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    # ### end Alembic commands ###
