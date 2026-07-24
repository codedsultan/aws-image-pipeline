variable "function_name" {
  description = "Name of the Lambda function this role belongs to"
  type        = string
}

variable "raw_bucket_arn" {
  description = "ARN of the raw upload bucket"
  type        = string
}

variable "processed_bucket_arn" {
  description = "ARN of the processed output bucket"
  type        = string
}

variable "sns_topic_arn" {
  description = "ARN of the SNS topic the Lambda publishes to"
  type        = string
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {}
}
