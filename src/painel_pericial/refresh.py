from __future__ import annotations

import json
from datetime import UTC, datetime

import boto3

from .config import settings


def request_refresh(source: str = "dashboard") -> bool:
    if not settings.refresh_queue_url:
        return False
    boto3.client("sqs", region_name=settings.aws_region).send_message(
        QueueUrl=settings.refresh_queue_url,
        MessageBody=json.dumps({"source": source, "requested_at": datetime.now(UTC).isoformat()}),
    )
    return True
