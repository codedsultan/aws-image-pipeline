terraform {
  required_version = ">= 1.7"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }

  # Local state for now (Phase 2). Moves to S3 + DynamoDB in Phase 8.
  # backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "image-pipeline"
      Environment = "dev"
      ManagedBy   = "terraform"
    }
  }
}
