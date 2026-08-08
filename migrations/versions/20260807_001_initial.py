"""initial cloud schema"""
from alembic import op
import sqlalchemy as sa

revision = "20260807_001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "processes",
        sa.Column("process_number", sa.String(length=64), primary_key=True),
        sa.Column("nickname", sa.Text(), nullable=False, server_default=""),
        sa.Column("client", sa.Text(), nullable=False, server_default=""),
        sa.Column("category", sa.Text(), nullable=False, server_default=""),
        sa.Column("active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("last_status", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("last_movement_date", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("last_movement_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("deadline", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("deadline_type", sa.String(length=64), nullable=False, server_default="SEM PRAZO"),
        sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="SEM PRAZO"),
        sa.Column("source_url", sa.Text(), nullable=False, server_default=""),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "movements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("process_number", sa.String(length=64), sa.ForeignKey("processes.process_number", ondelete="CASCADE"), nullable=False),
        sa.Column("movement_date", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("movement_text", sa.Text(), nullable=False),
        sa.Column("collected_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("process_number", "movement_date", "movement_text", name="uq_movement"),
    )
    op.create_index("ix_movements_process_number", "movements", ["process_number"])
    op.create_table(
        "alerts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("process_number", sa.String(length=64), sa.ForeignKey("processes.process_number", ondelete="CASCADE"), nullable=False),
        sa.Column("client", sa.Text(), nullable=False, server_default=""),
        sa.Column("movement_date", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("movement_text", sa.Text(), nullable=False, server_default=""),
        sa.Column("deadline", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("deadline_type", sa.String(length=64), nullable=False, server_default="SEM PRAZO"),
        sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="SEM PRAZO"),
        sa.Column("alert_type", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.UniqueConstraint("process_number", "movement_date", "movement_text", "alert_type", name="uq_alert"),
    )
    op.create_index("ix_alerts_process_number", "alerts", ["process_number"])


def downgrade() -> None:
    op.drop_index("ix_alerts_process_number", table_name="alerts")
    op.drop_table("alerts")
    op.drop_index("ix_movements_process_number", table_name="movements")
    op.drop_table("movements")
    op.drop_table("processes")
