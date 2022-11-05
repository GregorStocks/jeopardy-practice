"""initial

Revision ID: 5439551249f1
Revises: 
Create Date: 2022-11-05 11:55:58.598636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5439551249f1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("clues", "correct_count")
    op.drop_column("clues", "incorrect_count")
    op.drop_column("games", "is_practiced")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "games",
        sa.Column("is_practiced", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "clues",
        sa.Column("incorrect_count", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "clues",
        sa.Column("correct_count", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    # ### end Alembic commands ###
