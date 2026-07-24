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

## Project structure

```
terraform/
  modules/       # s3, iam, lambda, sns - reusable building blocks
  envs/dev/      # wires the modules together for the dev environment
src/
  handler.py                    # thin Lambda entrypoint
  models.py                     # pydantic request/response models
  config.py                     # pydantic-settings, reads env vars set by Terraform
  services/image_processor.py   # core business logic
  clients/aws_clients.py        # boto3 client factories, injected not hardcoded
tests/unit/                     # pytest + moto, no real AWS calls
```

## Local setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

## Tests

```bash
pytest tests/unit -v
```

Runs entirely against `moto` mocks — no AWS credentials required.

## Deploy

Requires Terraform and valid AWS credentials (`aws sts get-caller-identity`
should succeed).

```bash
cd terraform/envs/dev
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars: set account_suffix to something globally unique
terraform init
terraform apply
```

## Roadmap

Current focus is correctness and clean structure. Planned next:

- Observability: structured logs, custom CloudWatch metrics, alarms, a dashboard
- Resilience: dead-letter queue, retry limits, idempotency
- Security hardening: KMS encryption, TLS-only bucket policy, SSM-managed config
- CI/CD: GitHub Actions running tests and `terraform plan` on every PR

## Author

**Olusegun Ibraheem** — [@codedsultan](https://github.com/codedsultan)

This project is a public portfolio piece demonstrating Serverless image processing pipeline on AWS. 
The architecture, patterns, and code are open for review and discussion; 