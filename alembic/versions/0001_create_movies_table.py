"""create movies table

Revision ID: 0001_create_movies_table
Revises: 
Create Date: 2025-10-31 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_create_movies_table'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'movies',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('title', sa.Text, nullable=True),
        sa.Column('release_date', sa.Date, nullable=True),
        sa.Column('vote_average', sa.Float, nullable=True),
        sa.Column('vote_count', sa.BigInteger, nullable=True),
        sa.Column('popularity', sa.Float, nullable=True),
        sa.Column('original_language', sa.String(length=8), nullable=True),
    )


def downgrade():
    op.drop_table('movies')
