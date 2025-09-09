"""
Configuration management
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # S3 Configuration
    s3_bucket_name: str = os.getenv("S3_BUCKET_NAME", "")

    # CloudFront Configuration
    cloudfront_domain: str = os.getenv("CLOUDFRONT_DOMAIN", "")

    # Application Configuration
    app_name: str = "file-service"
    app_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # File Upload Configuration
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "104857600"))  # 100MB
    allowed_file_types: str = os.getenv("ALLOWED_FILE_TYPES",
                                        "image,document,spreadsheet,presentation,archive,video,audio,code")

    # Database Configuration (for future use)
    database_url: str = os.getenv("DATABASE_URL", "")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)"""
    return Settings()
