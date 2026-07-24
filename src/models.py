from pydantic import BaseModel, Field


class S3ObjectRef(BaseModel):
    bucket: str
    key: str


class ProcessingResult(BaseModel):
    """What the service layer returns; handler.py turns this into the SNS message."""

    source: S3ObjectRef
    destination: S3ObjectRef
    width: int
    height: int
    size_bytes: int
    status: str = Field(default="success")


class ProcessingError(BaseModel):
    source: S3ObjectRef
    error_type: str
    error_message: str
