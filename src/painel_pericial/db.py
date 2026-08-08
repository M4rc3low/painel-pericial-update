from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    pass


class Process(Base):
    __tablename__ = "processes"

    process_number: Mapped[str] = mapped_column(String(64), primary_key=True)
    nickname: Mapped[str] = mapped_column(Text, default="")
    client: Mapped[str] = mapped_column(Text, default="")
    category: Mapped[str] = mapped_column(Text, default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_status: Mapped[str] = mapped_column(String(64), default="")
    last_movement_date: Mapped[str] = mapped_column(String(16), default="")
    last_movement_text: Mapped[str] = mapped_column(Text, default="")
    deadline: Mapped[str] = mapped_column(String(16), default="")
    deadline_type: Mapped[str] = mapped_column(String(64), default="SEM PRAZO")
    risk_level: Mapped[str] = mapped_column(String(32), default="SEM PRAZO")
    source_url: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class Movement(Base):
    __tablename__ = "movements"
    __table_args__ = (UniqueConstraint("process_number", "movement_date", "movement_text", name="uq_movement"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    process_number: Mapped[str] = mapped_column(String(64), ForeignKey("processes.process_number", ondelete="CASCADE"), index=True)
    movement_date: Mapped[str] = mapped_column(String(16), default="")
    movement_text: Mapped[str] = mapped_column(Text)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


class Alert(Base):
    __tablename__ = "alerts"
    __table_args__ = (UniqueConstraint("process_number", "movement_date", "movement_text", "alert_type", name="uq_alert"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    process_number: Mapped[str] = mapped_column(String(64), ForeignKey("processes.process_number", ondelete="CASCADE"), index=True)
    client: Mapped[str] = mapped_column(Text, default="")
    movement_date: Mapped[str] = mapped_column(String(16), default="")
    movement_text: Mapped[str] = mapped_column(Text, default="")
    deadline: Mapped[str] = mapped_column(String(16), default="")
    deadline_type: Mapped[str] = mapped_column(String(64), default="SEM PRAZO")
    risk_level: Mapped[str] = mapped_column(String(32), default="SEM PRAZO")
    alert_type: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(engine)


def utcnow() -> datetime:
    return datetime.now(UTC)


def upsert_process(data: dict) -> None:
    with SessionLocal.begin() as session:
        obj = session.get(Process, data["process_number"]) or Process(process_number=data["process_number"])
        for key in ("nickname", "client", "category"):
            if key in data and data[key] is not None:
                setattr(obj, key, data[key])
        obj.last_status = data.get("status", "")
        obj.last_movement_date = data.get("last_movement_date", "")
        obj.last_movement_text = data.get("last_movement_text", "")
        obj.deadline = data.get("deadline", "")
        obj.deadline_type = data.get("deadline_type", "SEM PRAZO")
        obj.risk_level = data.get("risk_level", "SEM PRAZO")
        obj.source_url = data.get("source_url", "")
        obj.updated_at = utcnow()
        session.add(obj)


def add_movement_if_new(process_number: str, movement_date: str, movement_text: str) -> bool:
    with SessionLocal.begin() as session:
        existing = session.scalar(select(Movement.id).where(
            Movement.process_number == process_number,
            Movement.movement_date == movement_date,
            Movement.movement_text == movement_text,
        ))
        if existing:
            return False
        session.add(Movement(process_number=process_number, movement_date=movement_date, movement_text=movement_text))
        return True


def add_alert_if_new(data: dict) -> bool:
    with SessionLocal.begin() as session:
        existing = session.scalar(select(Alert.id).where(
            Alert.process_number == data["process_number"],
            Alert.movement_date == data.get("movement_date", ""),
            Alert.movement_text == data.get("movement_text", ""),
            Alert.alert_type == data["alert_type"],
        ))
        if existing:
            return False
        session.add(Alert(**data))
        return True


def active_processes() -> list[dict]:
    with SessionLocal() as session:
        rows = session.scalars(select(Process).where(Process.active.is_(True)).order_by(Process.process_number)).all()
        return [{
            "process_number": p.process_number,
            "nickname": p.nickname,
            "client": p.client,
            "category": p.category,
        } for p in rows]
