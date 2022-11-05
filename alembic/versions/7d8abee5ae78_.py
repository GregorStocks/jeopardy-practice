"""empty message

Revision ID: 7d8abee5ae78
Revises: d56ff33711cc
Create Date: 2022-11-05 11:43:54.459869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7d8abee5ae78"
down_revision = "d56ff33711cc"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("games", sa.Column("is_practiced", sa.Boolean(), default="false"))
    op.add_column("clues", sa.Column("correct_count", sa.Integer(), default="0"))
    op.add_column("clues", sa.Column("incorrect_count", sa.Integer(), default="0"))
