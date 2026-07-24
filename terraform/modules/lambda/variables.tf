variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "source_dir" {
  description = "Path to the directory containing handler.py and dependencies"
  type        = string
}

variable "role_arn" {
  description = "ARN of the IAM execution role"
  type        = string
}

variable "timeout" {
  description = "Function timeout in seconds"
  type        = number
  default     = 30
}

variable "memory_size" {
  description = "Function memory in MB"
  type        = number
  default     = 256
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 14
}

variable "environment_variables" {
  description = "Environment variables passed to the function"
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {}
}
