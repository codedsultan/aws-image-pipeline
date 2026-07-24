variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "ca-central-1"
}

variable "project_name" {
  description = "Short project name used in resource naming"
  type        = string
  default     = "image-pipeline"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "account_suffix" {
  description = "Short unique suffix (e.g. your AWS account ID last 6 digits) to keep S3 bucket names globally unique"
  type        = string
}

variable "notification_email" {
  description = "Email to subscribe to the SNS processing-complete topic (leave empty to skip)"
  type        = string
  default     = ""
}
