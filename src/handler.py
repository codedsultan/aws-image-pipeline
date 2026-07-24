from urllib.parse import unquote_plus

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from services.image_processor import ImageProcessor

logger = Logger(service="image-processor")


def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Entrypoint only: extract bucket/key from each S3 record and delegate.
    No image-processing logic lives here - see services/image_processor.py.
    Any unhandled exception propagates, which is what allows Lambda's
    built-in retry + DLQ behavior (Phase 7) to take over.
    """
    processor = ImageProcessor()
    results = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])

        logger.info("processing_started", extra={"bucket": bucket, "key": key})

        result = processor.process(bucket, key)
        results.append(result.model_dump())

        logger.info(
            "processing_completed",
            extra={"bucket": bucket, "key": key, "destination_key": result.destination.key},
        )

    return {"processed": len(results), "results": results}
