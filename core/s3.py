import boto3
import requests
from decouple import config


s3_client = boto3.client(
    "s3",
    aws_access_key_id=config("AWS_ACCESS_KEY"),
    aws_secret_access_key=config("AWS_SECRET_KEY"),
    region_name=config("AWS_REGION"),
)


def create_presigned_post(object_path, expiration=3600):
    file_name = object_path.split("/")[-1]

    response = s3_client.generate_presigned_post(
        config("S3_BUCKET_NAME"),
        file_name,
        ExpiresIn=expiration,
    )

    print(response)

    files = {"file": open(object_path, "rb")}

    r = requests.post(response["url"], data=response["fields"], files=files)

    return r.status_code
