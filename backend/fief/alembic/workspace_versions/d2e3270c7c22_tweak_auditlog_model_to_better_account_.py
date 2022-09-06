"""Tweak AuditLog model to better account for admin operations

Revision ID: d2e3270c7c22
Revises: c52822680356
Create Date: 2022-09-06 09:24:22.625912

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

import fief

# revision identifiers, used by Alembic.
revision = "d2e3270c7c22"
down_revision = "c52822680356"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "fief_audit_logs",
        sa.Column("admin_user_id", fief.models.generics.GUID(), nullable=True),
    )
    op.add_column(
        "fief_audit_logs",
        sa.Column("admin_api_key_id", fief.models.generics.GUID(), nullable=True),
    )

    connection = op.get_bind()
    if connection.dialect.name != "sqlite":
        op.drop_constraint(
            "fief_audit_logs_subject_user_id_fkey",
            "fief_audit_logs",
            type_="foreignkey",
        )
        op.drop_constraint(
            "fief_audit_logs_author_user_id_fkey", "fief_audit_logs", type_="foreignkey"
        )
    else:
        # Ref: https://alembic.sqlalchemy.org/en/latest/batch.html#dropping-unnamed-or-named-foreign-key-constraints
        naming_convention = {
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        }
        with op.batch_alter_table(
            "fief_audit_logs", naming_convention=naming_convention
        ) as batch_op:
            batch_op.drop_constraint(
                "fk_fief_audit_logs_subject_user_id_fief_users", type_="foreignkey"
            )
            batch_op.drop_constraint(
                "fk_fief_audit_logs_author_user_id_fief_users", type_="foreignkey"
            )

    op.drop_column("fief_audit_logs", "author_user_id")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "fief_audit_logs",
        sa.Column(
            "author_user_id", postgresql.UUID(), autoincrement=False, nullable=True
        ),
    )
    op.create_foreign_key(
        "fief_audit_logs_author_user_id_fkey",
        "fief_audit_logs",
        "fief_users",
        ["author_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_foreign_key(
        "fief_audit_logs_subject_user_id_fkey",
        "fief_audit_logs",
        "fief_users",
        ["subject_user_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("fief_audit_logs", "admin_api_key_id")
    op.drop_column("fief_audit_logs", "admin_user_id")
    # ### end Alembic commands ###
