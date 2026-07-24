variable "topic_name" {
  description = "Name of the SNS topic"
  type        = string
}

variable "notification_email" {
  description = "Email address to subscribe to the topic (leave empty to skip)"
  type        = string
  default     = ""
}

variable "publisher_role_arn" {
  description = "ARN of the IAM role allowed to publish to this topic"
  type        = string
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {}
}
