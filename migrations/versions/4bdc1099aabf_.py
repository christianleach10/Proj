"""empty message

Revision ID: 4bdc1099aabf
Revises: 
Create Date: 2021-11-12 12:45:41.661259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bdc1099aabf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('distance', sa.String(length=64), nullable=True),
    sa.Column('difficulty', sa.String(length=64), nullable=True),
    sa.Column('location', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trail_difficulty'), 'trail', ['difficulty'], unique=True)
    op.create_index(op.f('ix_trail_distance'), 'trail', ['distance'], unique=True)
    op.create_index(op.f('ix_trail_location'), 'trail', ['location'], unique=False)
    op.create_index(op.f('ix_trail_name'), 'trail', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_description'), 'user', ['description'], unique=False)
    op.create_index(op.f('ix_user_password'), 'user', ['password'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('trail_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['trail_id'], ['trail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trail_to_review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trail_id', sa.Integer(), nullable=True),
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ),
    sa.ForeignKeyConstraint(['trail_id'], ['trail.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_to_review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['review.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_to_review')
    op.drop_table('trail_to_review')
    op.drop_table('review')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_password'), table_name='user')
    op.drop_index(op.f('ix_user_description'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_trail_name'), table_name='trail')
    op.drop_index(op.f('ix_trail_location'), table_name='trail')
    op.drop_index(op.f('ix_trail_distance'), table_name='trail')
    op.drop_index(op.f('ix_trail_difficulty'), table_name='trail')
    op.drop_table('trail')
    # ### end Alembic commands ###
