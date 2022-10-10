try:
    from ..credentials import SECRET, ACCESS_KEY
except:
    print("Could not find credentials.py ... please ask for it")
    SECRET = None
    ACCESS_KEY = None
    is_anonymous = True
else:
    is_anonymous = False

import logging
import boto3
from botocore.exceptions import ClientError
import os
import typing as T


def upload_image(file_name: str) -> bool:
    return upload_file(file_name, bucket="patriaimages")

def download_image(remote_name: str, local_path: str) -> bool:
    s3_client = get_s3_client()
    try:
        response = s3_client.download_file("patriaimages", remote_name, local_path)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_s3_client():
    if is_anonymous:
        return boto3.client("s3")
    else:
        return boto3.client(
            "s3",
            aws_access_key_id = ACCESS_KEY,
            aws_secret_access_key = SECRET,
        )

def upload_file(file_name, bucket, object_name=None) -> bool:
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = get_s3_client()
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={
            "GrantRead": 'uri="http://acs.amazonaws.com/groups/global/AllUsers"',
        })
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_buckets():
    s3_client = get_s3_client()
    response = s3_client.list_buckets()
    return response["Buckets"]

