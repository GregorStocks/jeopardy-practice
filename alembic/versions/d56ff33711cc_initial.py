"""initial

Revision ID: d56ff33711cc
Revises: 
Create Date: 2022-01-09 15:26:52.389150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d56ff33711cc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category"),
    )
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), autoincrement=False, nullable=False),
        sa.Column("airdate", sa.String(), nullable=False),
        sa.Column("game_comments", sa.String(), nullable=True),
        sa.Column("game_type", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "clues",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("round", sa.Integer(), nullable=False),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("clue", sa.String(), nullable=False),
        sa.Column("answer", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["game_id"],
            ["games.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("clues")
    op.drop_table("games")
    op.drop_table("categories")