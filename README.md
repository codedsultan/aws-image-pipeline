# AWS Image Pipeline

Serverless image processing pipeline on AWS: an S3 upload triggers a Lambda
that generates a thumbnail and publishes a completion event via SNS.

## Architecture

```
S3 (raw/*) --ObjectCreated--> Lambda (image-processor) --> S3 (processed/*)
                                      |
                                      +--> SNS (image-processed topic)
```

- **Infrastructure as code** — the entire stack (S3 buckets, Lambda, IAM,
  SNS) is defined in Terraform and reproducible from a single `apply`.
- **Least-privilege IAM** — the Lambda's execution role is scoped to exact
  resource ARNs (`raw/*` for reads, `processed/*` for writes); no wildcard
  actions or resources anywhere in the policy.
- **Testable in isolation** — all AWS SDK calls are isolated behind a thin
  client layer, so the processing logic is fully unit-testable without live
  AWS credentials.

## Tech stack

Python 3.12 · Terraform · AWS (S3, Lambda, SNS, IAM, CloudWatch) · pydantic


## Author

**Olusegun Ibraheem** — [@codedsultan](https://github.com/codedsultan)

This project is a public portfolio piece demonstrating Serverless image processing pipeline on AWS. 
The architecture, patterns, and code are open for review and discussion; 