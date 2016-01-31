"""init migration

Revision ID: 1b0fff36c097
Revises: None
Create Date: 2016-01-31 18:37:25.804000

"""

# revision identifiers, used by Alembic.
revision = '1b0fff36c097'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commentacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('authorid', sa.Integer(), nullable=True),
    sa.Column('activityid', sa.Integer(), nullable=True),
    sa.Column('commentid', sa.Integer(), nullable=True),
    sa.Column('likenumber', sa.Integer(), nullable=True),
    sa.Column('commentnumber', sa.Integer(), nullable=True),
    sa.Column('disable', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['activityid'], ['activitys.id'], ),
    sa.ForeignKeyConstraint(['authorid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_commentacts_timestamp'), 'commentacts', ['timestamp'], unique=False)
    op.create_table('commentactimageattachs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commentid', sa.Integer(), nullable=False),
    sa.Column('imageid', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['commentid'], ['commentacts.id'], ),
    sa.ForeignKeyConstraint(['imageid'], ['imageurls.id'], ),
    sa.PrimaryKeyConstraint('id', 'commentid', 'imageid')
    )
    op.create_table('likecommentacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('commentid', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['commentid'], ['commentacts.id'], ),
    sa.ForeignKeyConstraint(['userid'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id', 'userid', 'commentid')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likecommentacts')
    op.drop_table('commentactimageattachs')
    op.drop_index(op.f('ix_commentacts_timestamp'), table_name='commentacts')
    op.drop_table('commentacts')
    ### end Alembic commands ###