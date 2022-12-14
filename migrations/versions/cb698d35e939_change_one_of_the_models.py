"""change one of the models

Revision ID: cb698d35e939
Revises: b7be7512263d
Create Date: 2022-08-15 13:41:55.266272

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cb698d35e939"
down_revision = "b7be7512263d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("resource", "owner_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("resource", "owner_id", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###
