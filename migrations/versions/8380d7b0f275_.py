"""empty message

Revision ID: 8380d7b0f275
Revises: c6ecc403918d
Create Date: 2023-03-27 08:54:33.144280

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8380d7b0f275'
down_revision = 'c6ecc403918d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
