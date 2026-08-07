provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project_name
      ManagedBy = "terraform-bootstrap"
      Portfolio = "cloud-architecture-case"
    }
  }
}

data "aws_caller_identity" "current" {}
