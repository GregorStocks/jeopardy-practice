"""initial tables

Revision ID: 8e17c7992631
Revises: 
Create Date: 2022-01-04 14:40:13.405447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8e17c7992631"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "airdates",
        sa.Column("game", sa.Integer, primary_key=True),
        sa.Column("airdate", sa.String(), nullable=False),
        sa.Column("game_comments", sa.String()),
        sa.Column("game_type", sa.String(), nullable=False),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("category", sa.String(), nullable=False, unique=True),
    )

    op.create_table(
        "clues",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("game", sa.Integer, sa.ForeignKey("airdates.game"), nullable=False),
        sa.Column("category", sa.Integer, sa.ForeignKey("categories.id"), nullable=False),
        sa.Column("round", sa.Integer, nullable=False),
        sa.Column("value", sa.Integer, nullable=False),
        sa.Column("clue", sa.String, nullable=False),
        sa.Column("answer", sa.String, nullable=False),
    )


def downgrade():
    pass
