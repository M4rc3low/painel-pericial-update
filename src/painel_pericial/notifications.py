from __future__ import annotations

import json

import boto3

from .config import settings


def publish_alert(alert: dict) -> None:
    if not settings.alert_topic_arn:
        return
    boto3.client("sns", region_name=settings.aws_region).publish(
        TopicArn=settings.alert_topic_arn,
        Subject=f"Painel Pericial - {alert['alert_type']}",
        Message=json.dumps(alert, ensure_ascii=False, default=str),
    )
