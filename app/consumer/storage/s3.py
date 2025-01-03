import boto3

from config.settings import settings


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.MINIO_ROOT_USER,
        aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
        endpoint_url=settings.MINIO_ENDPOINT
    )
