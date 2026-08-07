provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
      Portfolio   = "cloud-architecture-case"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_availability_zones" "available" { state = "available" }
data "aws_ecr_repository" "web" { name = "${var.project_name}-web" }
data "aws_ecr_repository" "worker" { name = "${var.project_name}-worker" }
