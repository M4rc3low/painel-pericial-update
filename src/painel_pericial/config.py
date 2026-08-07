from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import quote_plus


def _database_url() -> str:
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return explicit

    host = os.getenv("DB_HOST")
    if not host:
        return "sqlite:///./process_monitor.db"

    user = quote_plus(os.getenv("DB_USER", "painel"))
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "painel")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "local")
    database_url: str = _database_url()
    collector_mode: str = os.getenv("COLLECTOR_MODE", "public")
    collector_delay_seconds: float = float(os.getenv("COLLECTOR_DELAY_SECONDS", "1.5"))
    refresh_queue_url: str = os.getenv("REFRESH_QUEUE_URL", "")
    alert_topic_arn: str = os.getenv("ALERT_TOPIC_ARN", "")
    artifact_bucket: str = os.getenv("ARTIFACT_BUCKET", "")
    aws_region: str = os.getenv("AWS_REGION", "sa-east-1")


settings = Settings()
