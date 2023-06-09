"""empty message

Revision ID: 238a9c09de47
Revises: f221c6cd62cf
Create Date: 2023-03-29 10:28:08.545862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '238a9c09de47'
down_revision = 'f221c6cd62cf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coordinates', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_column('coordinates')

    # ### end Alembic commands ###
