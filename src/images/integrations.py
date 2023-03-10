from functools import lru_cache

import boto3
from attrs import define
from botocore.client import Config
from django.conf import settings

from .utils import assert_settings


@define
class S3Credentials:
    access_key_id: str
    secret_access_key: str
    region_name: str
    bucket_name: str
    default_acl: str
    presigned_expiry: int
    max_size: int


@lru_cache
def s3_get_credentials() -> S3Credentials:
    required_config = assert_settings(
        [
            "AWS_S3_ACCESS_KEY_ID",
            "AWS_S3_SECRET_ACCESS_KEY",
            "AWS_S3_REGION_NAME",
            "AWS_STORAGE_BUCKET_NAME",
            "AWS_DEFAULT_ACL",
            "AWS_PRESIGNED_EXPIRY",
            "FILE_MAX_SIZE",
        ],
        "S3 credentials not found.",
    )

    return S3Credentials(
        access_key_id=required_config["AWS_S3_ACCESS_KEY_ID"],
        secret_access_key=required_config["AWS_S3_SECRET_ACCESS_KEY"],
        region_name=required_config["AWS_S3_REGION_NAME"],
        bucket_name=required_config["AWS_STORAGE_BUCKET_NAME"],
        default_acl=required_config["AWS_DEFAULT_ACL"],
        presigned_expiry=required_config["AWS_PRESIGNED_EXPIRY"],
        max_size=required_config["FILE_MAX_SIZE"],
    )


def s3_get_client():
    credentials = s3_get_credentials()

    return boto3.client(
        service_name="s3",
        aws_access_key_id=credentials.access_key_id,
        aws_secret_access_key=credentials.secret_access_key,
        region_name=credentials.region_name,
        config=Config(s3={"addressing_style": "path"}, signature_version="s3v4"),
    )


def s3_generate_presigned_url(file_path, time):
    base = "https://" + settings.AWS_S3_CUSTOM_DOMAIN + "/"
    file_path = file_path.replace(base, "")

    credentials = s3_get_credentials()
    s3_client = s3_get_client()

    presigned_data = s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": credentials.bucket_name,
            "Key": file_path,
        },
        ExpiresIn=time,
    )

    return presigned_data
