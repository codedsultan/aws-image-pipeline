import os
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_DIR))

# Required Settings fields must exist before anything imports config.py
os.environ.setdefault("RAW_BUCKET", "test-raw-bucket")
os.environ.setdefault("PROCESSED_BUCKET", "test-processed-bucket")
os.environ.setdefault("SNS_TOPIC_ARN", "arn:aws:sns:ca-central-1:123456789012:test-topic")
os.environ.setdefault("AWS_DEFAULT_REGION", "ca-central-1")
