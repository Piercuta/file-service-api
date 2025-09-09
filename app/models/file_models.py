"""
Data models for file operations
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FileMetadata(BaseModel):
    """File metadata model"""
    id: str
    original_name: str
    content_type: Optional[str] = None
    size: int
    folder: Optional[str] = None
    uploaded_at: datetime
    s3_key: Optional[str] = None
    cloudfront_url: Optional[str] = None


class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    file_id: str
    filename: str
    size: int
    content_type: Optional[str] = None
    s3_key: str
    cloudfront_url: str
    uploaded_at: datetime


class FileListResponse(BaseModel):
    """Response model for file listing"""
    files: list[FileMetadata]
    total: int
    limit: int
    offset: int


class FileDeleteResponse(BaseModel):
    """Response model for file deletion"""
    message: str
    file_id: str

