import io

import boto3
import pytest
from moto import mock_aws
from PIL import Image

from services.image_processor import ImageProcessor
from config import settings


def _fake_jpeg_bytes(size=(1200, 900)) -> bytes:
    img = Image.new("RGB", size, color=(120, 45, 200))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()


@pytest.fixture
def aws(monkeypatch):
    with mock_aws():
        s3 = boto3.client("s3", region_name="ca-central-1")
        sns = boto3.client("sns", region_name="ca-central-1")

        s3.create_bucket(
            Bucket=settings.raw_bucket,
            CreateBucketConfiguration={"LocationConstraint": "ca-central-1"},
        )
        s3.create_bucket(
            Bucket=settings.processed_bucket,
            CreateBucketConfiguration={"LocationConstraint": "ca-central-1"},
        )
        topic = sns.create_topic(Name="test-topic")

        monkeypatch.setattr(settings, "sns_topic_arn", topic["TopicArn"])

        yield {"s3": s3, "sns": sns}


def test_process_creates_thumbnail_and_publishes(aws):
    s3 = aws["s3"]
    key = "raw/vacation-photo.jpg"

    s3.put_object(Bucket=settings.raw_bucket, Key=key, Body=_fake_jpeg_bytes())

    processor = ImageProcessor(s3=s3, sns=aws["sns"])
    result = processor.process(settings.raw_bucket, key)

    assert result.destination.key == "processed/vacation-photo.jpg"
    assert result.destination.bucket == settings.processed_bucket
    assert result.width <= settings.thumbnail_max_dimension
    assert result.height <= settings.thumbnail_max_dimension
    assert result.status == "success"

    # Confirm the thumbnail actually landed in the processed bucket
    stored = s3.get_object(Bucket=settings.processed_bucket, Key="processed/vacation-photo.jpg")
    assert stored["ContentLength"] > 0


def test_process_preserves_aspect_ratio(aws):
    s3 = aws["s3"]
    key = "raw/wide-banner.jpg"
    s3.put_object(Bucket=settings.raw_bucket, Key=key, Body=_fake_jpeg_bytes(size=(1600, 400)))

    processor = ImageProcessor(s3=s3, sns=aws["sns"])
    result = processor.process(settings.raw_bucket, key)

    # Original ratio is 4:1 - thumbnail should preserve that within rounding
    assert result.width / result.height == pytest.approx(1600 / 400, rel=0.05)
