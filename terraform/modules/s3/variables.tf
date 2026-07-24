variable "raw_bucket_name" {
  description = "Name of the bucket that receives uploaded images"
  type        = string
}

variable "processed_bucket_name" {
  description = "Name of the bucket that stores processed images"
  type        = string
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {}
}
