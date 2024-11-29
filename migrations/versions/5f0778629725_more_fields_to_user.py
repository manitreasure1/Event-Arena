"""more fields to user 

Revision ID: 5f0778629725
Revises: 445a3f251007
Create Date: 2024-11-25 02:28:30.168392

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f0778629725'
down_revision = '445a3f251007'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_login_at', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('last_login_ip', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_account', schema=None) as batch_op:
        batch_op.drop_column('last_login_ip')
        batch_op.drop_column('current_login_at')

    # ### end Alembic commands ###
