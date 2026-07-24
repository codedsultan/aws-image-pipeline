locals {
  function_name = "${var.project_name}-image-processor-${var.environment}"
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

module "s3" {
  source = "../../modules/s3"

  raw_bucket_name       = "${var.project_name}-raw-${var.environment}-${var.account_suffix}"
  processed_bucket_name = "${var.project_name}-processed-${var.environment}-${var.account_suffix}"
  tags                  = local.tags
}

module "sns" {
  source = "../../modules/sns"

  topic_name          = "${var.project_name}-image-processed-${var.environment}"
  notification_email  = var.notification_email
  publisher_role_arn  = module.iam.role_arn
  tags                = local.tags
}

module "iam" {
  source = "../../modules/iam"

  function_name         = local.function_name
  raw_bucket_arn         = module.s3.raw_bucket_arn
  processed_bucket_arn   = module.s3.processed_bucket_arn
  sns_topic_arn          = module.sns.topic_arn
  tags                   = local.tags
}

module "lambda" {
  source = "../../modules/lambda"

  function_name = local.function_name
  source_dir    = "${path.module}/../../../src"
  role_arn      = module.iam.role_arn

  environment_variables = {
    RAW_BUCKET       = module.s3.raw_bucket_name
    PROCESSED_BUCKET = module.s3.processed_bucket_name
    SNS_TOPIC_ARN    = module.sns.topic_arn
    LOG_LEVEL        = "INFO"
  }

  tags = local.tags
}

# Wired here (not inside the S3 module) to avoid a circular dependency:
# S3 notification needs the Lambda ARN, IAM needs the bucket ARNs,
# Lambda needs the IAM role ARN.
resource "aws_lambda_permission" "allow_s3_invoke" {
  statement_id  = "AllowExecutionFromS3"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.s3.raw_bucket_arn
}

resource "aws_s3_bucket_notification" "raw_upload_trigger" {
  bucket = module.s3.raw_bucket_id

  lambda_function {
    lambda_function_arn = module.lambda.function_arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "raw/"
  }

  depends_on = [aws_lambda_permission.allow_s3_invoke]
}
