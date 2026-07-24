import io
import json

from PIL import Image

from clients.aws_clients import s3_client, sns_client
from config import settings
from models import ProcessingResult, S3ObjectRef


class ImageProcessor:
    """
    Downloads an uploaded image, generates a thumbnail, stores it in the
    processed bucket, and publishes a completion notification.

    No AWS SDK calls should exist outside this class and clients/aws_clients.py -
    that's what makes this unit-testable without any real AWS credentials.
    """

    def __init__(self, s3=None, sns=None):
        self._s3 = s3 or s3_client()
        self._sns = sns or sns_client()

    def process(self, bucket: str, key: str) -> ProcessingResult:
        source = S3ObjectRef(bucket=bucket, key=key)

        raw_bytes = self._download(bucket, key)
        thumbnail_bytes, width, height = self._make_thumbnail(raw_bytes)

        dest_key = self._destination_key(key)
        self._upload(settings.processed_bucket, dest_key, thumbnail_bytes)

        destination = S3ObjectRef(bucket=settings.processed_bucket, key=dest_key)
        result = ProcessingResult(
            source=source,
            destination=destination,
            width=width,
            height=height,
            size_bytes=len(thumbnail_bytes),
        )

        self._publish(result)
        return result

    def _download(self, bucket: str, key: str) -> bytes:
        response = self._s3.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()

    def _make_thumbnail(self, raw_bytes: bytes) -> tuple[bytes, int, int]:
        with Image.open(io.BytesIO(raw_bytes)) as img:
            img = img.convert("RGB")
            img.thumbnail((settings.thumbnail_max_dimension, settings.thumbnail_max_dimension))

            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            return buffer.getvalue(), img.width, img.height

    def _upload(self, bucket: str, key: str, body: bytes) -> None:
        self._s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=body,
            ContentType="image/jpeg",
            ServerSideEncryption="AES256",
        )

    def _publish(self, result: ProcessingResult) -> None:
        self._sns.publish(
            TopicArn=settings.sns_topic_arn,
            Subject="Image processing complete",
            Message=json.dumps(result.model_dump()),
        )

    @staticmethod
    def _destination_key(raw_key: str) -> str:
        # raw/photo.jpg -> processed/photo.jpg
        filename = raw_key.split("/")[-1]
        return f"processed/{filename}"
