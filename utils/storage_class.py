import os
import boto3
from botocore.exceptions import NoCredentialsError,ClientError
from dotenv import load_dotenv

class S3Wrapper:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        region_name = 'us-east-1'  # Set the region
        self.bucket_name = 'rearc-datalake-bucket'  # Set the bucket name

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

    def upload_file(self, file_name, object_name=None):
        """Upload a file to the S3 bucket"""
        if object_name is None:
            object_name = file_name
        try:
            self.s3_client.upload_file(file_name, self.bucket_name, object_name)
            print(f"File {file_name} uploaded to {self.bucket_name}/{object_name}")
        except NoCredentialsError:
            print("Credentials not available")

    def list_bucket_contents(self):
        """List files in the S3 bucket"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            return [item['Key'] for item in response.get('Contents', [])]
        except NoCredentialsError:
            print("Credentials not available")
            return []
        
    def delete_file(self, object_name):
        """Delete a file from the S3 bucket."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file {object_name}: {e}")



