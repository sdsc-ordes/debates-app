import boto3
import os

from dotenv import load_dotenv

load_dotenv()

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION_NAME = os.getenv("S3_REGION_NAME")
DEV_S3_ACCESS_KEY = os.getenv("DEV_S3_ACCESS_KEY")
DEV_S3_SECRET_KEY = os.getenv("DEV_S3_SECRET_KEY")
DEV_S3_BUCKET_NAME = os.getenv("DEV_S3_BUCKET_NAME")
DEV_S3_SERVER = os.getenv("DEV_S3_SERVER")


class s3Manager:
    def __init__(self, dev):
        if dev:
            self.s3 = boto3.client(
                's3',
                endpoint_url=DEV_S3_SERVER,
                aws_access_key_id=DEV_S3_ACCESS_KEY,
                aws_secret_access_key=DEV_S3_SECRET_KEY
            )
            self.bucket_name = DEV_S3_BUCKET_NAME
        else:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_KEY,
                region_name=S3_REGION_NAME
            )
            self.bucket_name = S3_BUCKET_NAME

    def test_connection(self):
        self.s3.head_bucket(Bucket=self.bucket_name)
        print("connection to s3 established")

    def list_bucket_content(self, prefix=None):
        paginator = self.s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
            if prefix:
                print(f"Content of bucket {self.bucket_name} with prefix '{prefix}':")
            else:
                print(f"Content of bucket {self.bucket_name}:")
            _print_objects_for_s3_page(page)

    def get_s3_data(self, s3_path):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_path)
        data = response['Body'].read().decode('utf-8')
        return data


def _print_objects_for_s3_page(page):
    for obj in page.get('Contents', []):
        key = obj['Key']
        print(key)
