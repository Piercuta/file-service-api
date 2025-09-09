"""
CloudFront service for file URL generation
"""

import logging
from typing import Optional
from .config import get_settings

logger = logging.getLogger(__name__)


class CloudFrontService:
    """Service for CloudFront operations"""

    def __init__(self):
        self.settings = get_settings()
        self.cloudfront_domain = self.settings.cloudfront_domain

    def get_file_url(self, s3_key: str) -> str:
        """
        Generate CloudFront URL for a file

        Args:
            s3_key: S3 object key

        Returns:
            CloudFront URL for the file
        """
        if not self.cloudfront_domain:
            logger.warning("CloudFront domain not configured, using S3 URL")
            return f"https://{self.settings.s3_bucket_name}.s3.{self.settings.aws_region}.amazonaws.com/{s3_key}"

        # Remove leading slash if present
        s3_key = s3_key.lstrip('/')

        # Construct CloudFront URL
        cloudfront_url = f"https://{self.cloudfront_domain}/{s3_key}"

        logger.info(f"Generated CloudFront URL: {cloudfront_url}")
        return cloudfront_url

    def get_signed_url(
        self,
        s3_key: str,
        expiration: int = 3600
    ) -> str:
        """
        Generate signed CloudFront URL (requires CloudFront key pair)

        Args:
            s3_key: S3 object key
            expiration: URL expiration time in seconds

        Returns:
            Signed CloudFront URL
        """
        # This would require CloudFront key pair configuration
        # For now, return regular CloudFront URL
        logger.warning("Signed URLs not implemented, returning regular URL")
        return self.get_file_url(s3_key)

