import boto3
import os

from dotenv import load_dotenv

load_dotenv()

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_SERVER = os.getenv("S3_SERVER")


class s3Manager:
    def __init__(self):
        self.s3 = boto3.client('s3',
                               endpoint_url=S3_SERVER,
                               aws_access_key_id=S3_ACCESS_KEY,
                               aws_secret_access_key=S3_SECRET_KEY
                               )
        self.bucket_name = S3_BUCKET_NAME

    def test_connection(self):
        self.s3.head_bucket(Bucket=self.bucket_name)
        print("connection to s3 established")

    def list_objects(self):
        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Delimiter='/'
        )
        folders = []
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                folders.append(prefix['Prefix'])
        print(folders)

    def get_srt_file_for_object(self, s3_path):
        object_key = f"{s3_path}/{s3_path}.srt"
        response = self.s3.get_object(Bucket=self.bucket_name, Key=object_key)
        srt_data = response['Body'].read().decode('utf-8')
        return srt_data
