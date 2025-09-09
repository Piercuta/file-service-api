"""
S3 service for file operations
"""

import boto3
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import UploadFile
from botocore.exceptions import ClientError, NoCredentialsError
from ..utils.config import get_settings

logger = logging.getLogger(__name__)


class S3Service:
    """Service for S3 operations"""

    def __init__(self):
        self.settings = get_settings()
        self.s3_client = boto3.client('s3')
        self.bucket_name = self.settings.s3_bucket_name

    async def upload_file(
        self,
        file: UploadFile,
        file_id: str,
        folder: Optional[str] = None
    ) -> str:
        """
        Upload file to S3 bucket

        Args:
            file: FastAPI UploadFile object
            file_id: Unique file identifier
            folder: Optional folder path in S3

        Returns:
            S3 key of uploaded file
        """
        try:
            # Construct S3 key
            if folder:
                s3_key = f"{folder}/{file_id}"
            else:
                s3_key = f"files/{file_id}"

            # Read file content
            file_content = await file.read()
            uploaded_at = datetime.utcnow().isoformat()
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=file.content_type,
                Metadata={
                    'original_name': file.filename,
                    'file_id': file_id,
                    'uploaded_at': uploaded_at
                }
            )

            logger.info(f"File uploaded to S3: {s3_key}")
            return s3_key

        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise Exception("AWS credentials not configured")
        except ClientError as e:
            logger.error(f"S3 upload error: {str(e)}")
            raise Exception(f"Failed to upload file to S3: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during upload: {str(e)}")
            raise Exception(f"Upload failed: {str(e)}")

    async def file_exists(self, s3_key: str) -> bool:
        """
        Check if file exists in S3

        Args:
            s3_key: S3 object key

        Returns:
            True if file exists, False otherwise
        """
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise Exception(f"Error checking file existence: {str(e)}")

    async def get_file_metadata(self, s3_key: str) -> Dict[str, Any]:
        """
        Get file metadata from S3

        Args:
            s3_key: S3 object key

        Returns:
            Dictionary containing file metadata
        """
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)

            return {
                's3_key': s3_key,
                'content_type': response.get('ContentType'),
                'size': response.get('ContentLength'),
                'last_modified': response.get('LastModified'),
                'metadata': response.get('Metadata', {})
            }

        except ClientError as e:
            logger.error(f"Error getting file metadata: {str(e)}")
            raise Exception(f"Failed to get file metadata: {str(e)}")

    async def delete_file(self, s3_key: str) -> bool:
        """
        Delete file from S3

        Args:
            s3_key: S3 object key

        Returns:
            True if deletion successful
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            logger.info(f"File deleted from S3: {s3_key}")
            return True

        except ClientError as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise Exception(f"Failed to delete file: {str(e)}")

    async def generate_presigned_url(
        self,
        s3_key: str,
        expiration: int = 3600
    ) -> str:
        """
        Generate presigned URL for file access

        Args:
            s3_key: S3 object key
            expiration: URL expiration time in seconds

        Returns:
            Presigned URL
        """
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url

        except ClientError as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            raise Exception(f"Failed to generate presigned URL: {str(e)}")

    async def list_files(
        self,
        prefix: str = "files/",
        max_keys: int = 1000
    ) -> list[Dict[str, Any]]:
        """
        List files in S3 bucket

        Args:
            prefix: S3 key prefix to filter files
            max_keys: Maximum number of files to return

        Returns:
            List of file metadata dictionaries
        """
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=max_keys
            )

            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'],
                        'etag': obj['ETag']
                    })

            return files

        except ClientError as e:
            logger.error(f"Error listing files: {str(e)}")
            raise Exception(f"Failed to list files: {str(e)}")
