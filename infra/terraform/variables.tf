variable "aws_region" {
  type    = string
  default = "sa-east-1"
}

variable "project_name" {
  type    = string
  default = "painel-pericial"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "schedule_expression" {
  type    = string
  default = "rate(1 hour)"
}

variable "collector_delay_seconds" {
  type    = number
  default = 1.5
}

variable "web_desired_count" {
  type    = number
  default = 1
}

variable "web_min_capacity" {
  type    = number
  default = 1
}

variable "web_max_capacity" {
  type    = number
  default = 2
}

variable "db_instance_class" {
  type    = string
  default = "db.t4g.micro"
}

variable "db_engine_version" {
  type     = string
  default  = null
  nullable = true
}

variable "db_multi_az" {
  type    = bool
  default = false
}

variable "db_deletion_protection" {
  type    = bool
  default = false
}

variable "certificate_arn" {
  type     = string
  default  = null
  nullable = true
}

variable "enable_waf" {
  type    = bool
  default = false
}

variable "ops_email" {
  type     = string
  default  = null
  nullable = true
}

variable "monthly_budget_usd" {
  type    = number
  default = 60
}

variable "enable_cognito_auth" {
  type    = bool
  default = false
}

variable "app_fqdn" {
  type     = string
  default  = null
  nullable = true
}

variable "hosted_zone_id" {
  type     = string
  default  = null
  nullable = true
}

variable "nat_gateway_mode" {
  type    = string
  default = "single"

  validation {
    condition     = contains(["single", "per_az"], var.nat_gateway_mode)
    error_message = "nat_gateway_mode must be single or per_az."
  }
}
