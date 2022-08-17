"""set user role to not null

Revision ID: 2c771ada2136
Revises: af886e11c1b7
Create Date: 2022-08-17 08:48:43.258947

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2c771ada2136'
down_revision = 'af886e11c1b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_role',
               existing_type=postgresql.ENUM('user', 'admin', name='userrole'),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'user_role',
               existing_type=postgresql.ENUM('user', 'admin', name='userrole'),
               nullable=True)
    # ### end Alembic commands ###
