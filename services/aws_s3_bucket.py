import boto3
from botocore.exceptions import ClientError
from decouple import config
from werkzeug.exceptions import InternalServerError


class S3Service:
    """
    A class that will take care of the AWS S3 Bucket integration
    """
    def __init__(self):
        key = config("AWS_ACCESS_KEY_ID")
        secret = config("AWS_SECRET_KEY")
        self.region = config("AWS_S3_BUCKET_REGION")
        self.bucket = config("AWS_S3_BUCKET_NAME")
        self.s3 = boto3.client(
            "s3",
            region_name=self.region,
            aws_access_key_id=key,
            aws_secret_access_key=secret,
        )

    def upload_file(self, path, key):
        """
        Upload a file to the S3 bucket.

        :param path: string, the path to the file's current location
        :param key: string, access key to the S3 bucket
        :return: url: string, a link to the location of the file in the S3 bucket
        """
        try:
            self.s3.upload_file(path, self.bucket, key)
            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{key}"
        except ClientError as ex:
            raise InternalServerError(
                "Sorry, the S3 bucket service is not available at the moment, please try a bit later \N{unamused face}"
            )

    def delete_file(self, key):
        """
        Delete a file from the S3 bucket.

        :param key: string, access key to the S3 bucket
        :return: string message with the request status
        """
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=key)
            return "The file is now gone forever \N{unamused face}"
        except ClientError as ex:
            raise InternalServerError(
                "Sorry, the S3 bucket service is not available at the moment, please try a bit later \N{unamused face}"
            )
