data "aws_iam_policy_document" "assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name               = "${var.function_name}-exec-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
  tags               = var.tags
}

# Basic CloudWatch Logs permissions (AWS-managed, scoped by AWS to logs only)
resource "aws_iam_role_policy_attachment" "basic_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Everything below is scoped to exact resource ARNs - no wildcards.
data "aws_iam_policy_document" "lambda_permissions" {
  statement {
    sid    = "ReadRawBucket"
    effect = "Allow"
    actions = [
      "s3:GetObject",
    ]
    resources = ["${var.raw_bucket_arn}/raw/*"]
  }

  statement {
    sid    = "WriteProcessedBucket"
    effect = "Allow"
    actions = [
      "s3:PutObject",
    ]
    resources = ["${var.processed_bucket_arn}/processed/*"]
  }

  statement {
    sid       = "PublishProcessingComplete"
    effect    = "Allow"
    actions   = ["sns:Publish"]
    resources = [var.sns_topic_arn]
  }
}

resource "aws_iam_role_policy" "lambda_permissions" {
  name   = "${var.function_name}-permissions"
  role   = aws_iam_role.lambda_exec.id
  policy = data.aws_iam_policy_document.lambda_permissions.json
}
