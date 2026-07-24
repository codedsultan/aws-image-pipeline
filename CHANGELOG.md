# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Terraform infrastructure: S3 (raw/processed buckets), IAM (least-privilege
  Lambda execution role), Lambda, and SNS modules, composed for the dev
  environment
- Lambda service layer: thin `handler.py` entrypoint, pydantic request/result
  models, `pydantic-settings`-based config, injected boto3 client factories,
  and `ImageProcessor` for thumbnail generation and SNS notification
- Setup, testing, and deploy instructions in the README
