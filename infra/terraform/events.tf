resource "aws_sqs_queue" "refresh_dlq" {
  name                      = "${var.project_name}-${var.environment}-refresh-dlq"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true
}

resource "aws_sqs_queue" "refresh" {
  name                       = "${var.project_name}-${var.environment}-refresh"
  visibility_timeout_seconds = 120
  sqs_managed_sse_enabled    = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.refresh_dlq.arn
    maxReceiveCount     = 3
  })
}

data "archive_file" "trigger_worker" {
  type        = "zip"
  source_file = "${path.module}/../lambda/trigger_worker.py"
  output_path = "${path.module}/trigger_worker.zip"
}

resource "aws_iam_role" "trigger_lambda" {
  name = "${var.project_name}-${var.environment}-trigger-lambda"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "trigger_lambda_logs" {
  role       = aws_iam_role.trigger_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "trigger_lambda" {
  role = aws_iam_role.trigger_lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["ecs:ListTasks"]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = ["ecs:RunTask"]
        Resource = aws_ecs_task_definition.worker.arn
      },
      {
        Effect = "Allow"
        Action = ["iam:PassRole"]
        Resource = [
          aws_iam_role.task_execution.arn,
          aws_iam_role.worker_task.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = aws_sqs_queue.refresh.arn
      }
    ]
  })
}

resource "aws_lambda_function" "trigger_worker" {
  function_name                  = "${var.project_name}-${var.environment}-trigger-worker"
  role                           = aws_iam_role.trigger_lambda.arn
  handler                        = "trigger_worker.handler"
  runtime                        = "python3.12"
  filename                       = data.archive_file.trigger_worker.output_path
  source_code_hash               = data.archive_file.trigger_worker.output_base64sha256
  timeout                        = 30
  reserved_concurrent_executions = 1

  environment {
    variables = {
      ECS_CLUSTER_ARN            = aws_ecs_cluster.main.arn
      WORKER_TASK_DEFINITION_ARN = aws_ecs_task_definition.worker.arn
      WORKER_TASK_FAMILY         = aws_ecs_task_definition.worker.family
      WORKER_SUBNET_IDS          = join(",", aws_subnet.app[*].id)
      WORKER_SECURITY_GROUP_IDS  = aws_security_group.worker.id
    }
  }
}

resource "aws_lambda_event_source_mapping" "refresh" {
  event_source_arn = aws_sqs_queue.refresh.arn
  function_name    = aws_lambda_function.trigger_worker.arn
  batch_size       = 1
}

resource "aws_iam_role" "scheduler" {
  name = "${var.project_name}-${var.environment}-scheduler"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "scheduler.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "scheduler" {
  role = aws_iam_role.scheduler.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["lambda:InvokeFunction"]
      Resource = aws_lambda_function.trigger_worker.arn
    }]
  })
}

resource "aws_scheduler_schedule" "collector" {
  name                = "${var.project_name}-${var.environment}-collector"
  schedule_expression = var.schedule_expression

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = aws_lambda_function.trigger_worker.arn
    role_arn = aws_iam_role.scheduler.arn
  }
}

resource "aws_lambda_permission" "scheduler" {
  statement_id  = "AllowEventBridgeScheduler"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.trigger_worker.function_name
  principal     = "scheduler.amazonaws.com"
  source_arn    = aws_scheduler_schedule.collector.arn
}
