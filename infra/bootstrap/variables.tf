variable "aws_region" {
  type    = string
  default = "sa-east-1"
}

variable "project_name" {
  type    = string
  default = "painel-pericial"
}

variable "github_owner" {
  type    = string
  default = "M4rc3low"
}

variable "github_repository" {
  type    = string
  default = "painel-pericial-update"
}

variable "github_environments" {
  type    = list(string)
  default = ["aws-dev", "aws-prod"]
}
