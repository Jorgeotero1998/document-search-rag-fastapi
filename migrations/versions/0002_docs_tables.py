"""docs tables

Revision ID: 0002_docs_tables
Revises: 0001_init_users
Create Date: 2026-07-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_docs_tables"
down_revision = "0001_init_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "docs_documents",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    # Full text search index (expression GIN index)
    op.execute(
        "CREATE INDEX ix_docs_documents_content_fts ON docs_documents USING GIN (to_tsvector('simple', content));"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_docs_documents_content_fts;")
    op.drop_table("docs_documents")

