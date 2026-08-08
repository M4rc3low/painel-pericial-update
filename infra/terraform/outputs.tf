output "application_url" {
  value = var.app_fqdn != null ? "https://${var.app_fqdn}" : (var.certificate_arn == null ? "http://${aws_lb.web.dns_name}" : "https://${aws_lb.web.dns_name}")
}

output "alb_dns_name" {
  value = aws_lb.web.dns_name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "rds_endpoint" {
  value     = aws_db_instance.main.address
  sensitive = true
}

output "refresh_queue_url" {
  value = aws_sqs_queue.refresh.url
}

output "artifact_bucket" {
  value = aws_s3_bucket.artifacts.bucket
}

output "cloudwatch_dashboard" {
  value = aws_cloudwatch_dashboard.main.dashboard_name
}
