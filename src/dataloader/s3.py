import boto3
import os
from botocore.exceptions import NoCredentialsError, DataNotFoundError
from botocore.client import Config

from dotenv import load_dotenv

load_dotenv()

PROD_S3_ACCESS_KEY = os.getenv("PROD_S3_ACCESS_KEY")
PROD_S3_SECRET_KEY = os.getenv("PROD_S3_SECRET_KEY")
PROD_S3_BUCKET_NAME = os.getenv("PROD_S3_BUCKET_NAME")
PROD_S3_REGION_NAME = os.getenv("PROD_S3_REGION_NAME")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_SERVER = os.getenv("S3_SERVER")
S3_FRONTEND_BASE_URL = os.getenv("S3_FRONTEND_BASE_URL")
SUFFIX_SRT_ORIG = os.getenv("SUFFIX_SRT_ORIG")
SUFFIX_SRT_EN = os.getenv("SUFFIX_SRT_EN")
SUFFIX_METADATA = os.getenv("SUFFIX_METADATA")


class s3Manager:
    def __init__(self, prod=False):
        if prod:
            self.s3 = boto3.client(
                's3',
                aws_access_key_id=PROD_S3_ACCESS_KEY,
                aws_secret_access_key=PROD_S3_SECRET_KEY,
                region_name=PROD_S3_REGION_NAME
            )
            self.bucket_name = PROD_S3_BUCKET_NAME
        else:
            self.s3 = boto3.client(
                's3',
                endpoint_url=S3_SERVER,
                aws_access_key_id=S3_ACCESS_KEY,
                aws_secret_access_key=S3_SECRET_KEY,
            )
            self.bucket_name = "debates"

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
            # Loop through the contents and print the key and last modified date
            for obj in page.get('Contents', []):
                key = obj['Key']
                last_modified = obj['LastModified']
                print(f"Key: {key}, Last Modified: {last_modified}")

    def get_s3_data(self, s3_path):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=s3_path)
        data = response['Body'].read().decode('utf-8')
        return data

    def download_s3_data(self, s3_path, file):
        self.s3.download_file(self.bucket_name, s3_path, file)

    def get_presigned_url(self, prefix, key, expiration=3600):
        """
        Generate a presigned URL for an S3 object.
        """
        try:
            object_key = f"{prefix}/{key}"
            print(f"uploading data for s3 key {object_key}")
            response = self.s3.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": object_key,
                    "ResponseContentDisposition": f"attachment; filename={object_key}"
                },
                ExpiresIn=expiration,
            )
            frontend_url = response.replace(S3_SERVER, S3_FRONTEND_BASE_URL)
            return frontend_url
        except DataNotFoundError:
            print(f"s3 key not found: {object_key}")
        except NoCredentialsError:
            print("Credentials not available.")
            return None

    def upload_data(self, file_path, s3_path):
        """
        Uploads a file to the S3 bucket.

        :param file_path: Path to the file to upload (local file).
        :param s3_path: Path in the S3 bucket where the file should be uploaded.
        :raises NoCredentialsError: If credentials are invalid or missing.
        """
        try:
            self.s3.upload_file(file_path, self.bucket_name, s3_path)
            print(f"File '{file_path}' successfully uploaded to '{s3_path}' in bucket '{self.bucket_name}'.")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except NoCredentialsError:
            print("Error: Credentials are not available.")
        except Exception as e:
            print(f"An error occurred: {e}")
