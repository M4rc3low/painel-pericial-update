output "terraform_state_bucket" { value = aws_s3_bucket.terraform_state.bucket }
output "github_deploy_role_arn" { value = aws_iam_role.github_deploy.arn }
output "web_ecr_repository_url" { value = aws_ecr_repository.web.repository_url }
output "worker_ecr_repository_url" { value = aws_ecr_repository.worker.repository_url }
