output "raw_bucket_name" {
  value = module.s3.raw_bucket_name
}

output "processed_bucket_name" {
  value = module.s3.processed_bucket_name
}

output "lambda_function_name" {
  value = module.lambda.function_name
}

output "sns_topic_arn" {
  value = module.sns.topic_arn
}
