import json
import os

import boto3


ecs = boto3.client("ecs")


def _existing_tasks() -> list[str]:
    cluster = os.environ["ECS_CLUSTER_ARN"]
    family = os.environ["WORKER_TASK_FAMILY"]
    task_arns: list[str] = []
    for status in ("RUNNING", "PENDING"):
        response = ecs.list_tasks(cluster=cluster, family=family, desiredStatus=status)
        task_arns.extend(response.get("taskArns", []))
    return task_arns


def handler(event, context):
    existing = _existing_tasks()
    if existing:
        return {"started": [], "reason": "worker_already_running", "existing": existing}

    response = ecs.run_task(
        cluster=os.environ["ECS_CLUSTER_ARN"],
        taskDefinition=os.environ["WORKER_TASK_DEFINITION_ARN"],
        launchType="FARGATE",
        count=1,
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": os.environ["WORKER_SUBNET_IDS"].split(","),
                "securityGroups": os.environ["WORKER_SECURITY_GROUP_IDS"].split(","),
                "assignPublicIp": "DISABLED",
            }
        },
    )
    failures = response.get("failures", [])
    if failures:
        raise RuntimeError(json.dumps(failures))
    return {"started": [task["taskArn"] for task in response.get("tasks", [])]}
