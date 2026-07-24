from functools import lru_cache

import boto3


@lru_cache(maxsize=1)
def s3_client():
    return boto3.client("s3")


@lru_cache(maxsize=1)
def sns_client():
    return boto3.client("sns")
