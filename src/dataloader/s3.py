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

    def list_videos(self):
        response = self.s3.list_objects_v2(
            Bucket=self.bucket_name,
            Delimiter='/'
        )
        folders = []
        if 'CommonPrefixes' in response:
            for prefix in response['CommonPrefixes']:
                folders.append(prefix['Prefix'])
        print(folders)
        for folder in folders:
            result = self.s3.list_objects(Bucket=self.bucket_name, Prefix=folder, Delimiter='/')
            import pdb; pdb.set_trace()
            for o in result.get('CommonPrefixes'):
                print(f"sub folder : {o.get('Prefix')}")

    def get_keys_for_s3_name(self, s3_name):
        video_prefix = f"{s3_name}/"
        keys = []
        result = self.s3.list_objects(
            Bucket=self.bucket_name, Prefix=video_prefix, Delimiter='/'
        )
        for item in result.get('Contents', []):
            keys.append(item.get("Key"))
        return keys

    def get_srt_file_for_object(self, s3_name):
        keys = self.get_keys_for_s3_name(s3_name)
        srt_keys = [k for k in keys if k.endswith(".srt")]
        if srt_keys:
            srt_key = srt_keys[0]
        response = self.s3.get_object(Bucket=self.bucket_name, Key=srt_key)
        srt_data = response['Body'].read().decode('utf-8')
        return srt_data

    def get_metadata_for_object(self, s3_name):
        keys = self.get_keys_for_s3_name(s3_name)
        yml_keys = [k for k in keys if k.endswith(".yml")]
        if yml_keys:
            yml_key = yml_keys[0]
        response = self.s3.get_object(Bucket=self.bucket_name, Key=yml_key)
        metadata = response['Body'].read().decode('utf-8')
        return metadata
