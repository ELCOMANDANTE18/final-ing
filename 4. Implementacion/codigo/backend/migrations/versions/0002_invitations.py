"""Tabla invitations (CU0010 Invitación a la aplicación)

Revision ID: 0002_invitations
Revises: 0001_users
Create Date: 2026-11-26
"""
from alembic import op
import sqlalchemy as sa


revision = '0002_invitations'
down_revision = '0001_users'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'invitations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=254), nullable=False),
        sa.Column('inviter_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=16), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['inviter_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('invitations', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_invitations_email'), ['email'], unique=False)
        batch_op.create_index(batch_op.f('ix_invitations_inviter_id'), ['inviter_id'], unique=False)


def downgrade():
    with op.batch_alter_table('invitations', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_invitations_inviter_id'))
        batch_op.drop_index(batch_op.f('ix_invitations_email'))
    op.drop_table('invitations')
