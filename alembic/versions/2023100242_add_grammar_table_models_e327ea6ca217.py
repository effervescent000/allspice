"""add grammar table models

Revision ID: e327ea6ca217
Revises: 527ee33afb14
Create Date: 2023-10-02 22:42:45.333563

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e327ea6ca217"
down_revision = "527ee33afb14"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "grammar_table_model",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("part_of_speech", sa.String(), nullable=False),
        sa.Column("language_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["language_id"], ["language_model.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "grammar_table_cell_model",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("row_categories", sa.String(), nullable=False),
        sa.Column("column_categories", sa.String(), nullable=False),
        sa.Column("grammar_table_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["grammar_table_id"], ["grammar_table_model.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "grammar_table_column_model",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("grammar_table_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["grammar_table_id"], ["grammar_table_model.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "grammar_table_row_model",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
        sa.Column("grammar_table_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["grammar_table_id"], ["grammar_table_model.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "word_class_to_grammar_table",
        sa.Column("word_class_id", sa.Integer(), nullable=False),
        sa.Column("grammar_table_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["grammar_table_id"], ["grammar_table_model.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["word_class_id"], ["word_class_model.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("word_class_id", "grammar_table_id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("word_class_to_grammar_table")
    op.drop_table("grammar_table_row_model")
    op.drop_table("grammar_table_column_model")
    op.drop_table("grammar_table_cell_model")
    op.drop_table("grammar_table_model")
    # ### end Alembic commands ###
