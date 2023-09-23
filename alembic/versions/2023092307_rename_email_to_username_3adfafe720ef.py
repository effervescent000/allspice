"""rename email to username

Revision ID: 3adfafe720ef
Revises: 07c71f4389b6
Create Date: 2023-09-23 18:07:56.379571

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "3adfafe720ef"
down_revision = "07c71f4389b6"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("user_model", "email", new_column_name="username")


def downgrade():
    op.alter_column("user_model", "username", new_column_name="email")
