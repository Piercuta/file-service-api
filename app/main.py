"""
File Service - FastAPI microservice for file operations
Handles file upload, download, and metadata management with S3 and CloudFront
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from typing import List, Optional
import logging
import os
from datetime import datetime
import uuid

from .models.file_models import FileMetadata, FileUploadResponse, FileListResponse
from .services.s3_service import S3Service
from .services.cloudfront_service import CloudFrontService
from .utils.validators import validate_file_type, validate_file_size
from .utils.config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="File Service",
    description="Microservice for file upload, download and management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
settings = get_settings()
s3_service = S3Service()
cloudfront_service = CloudFrontService()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    folder: Optional[str] = Query(None, description="Optional folder path in S3")
):
    """
    Upload a file to S3 bucket
    """
    try:
        # Validate file
        if not validate_file_type(file.filename):
            raise HTTPException(status_code=400, detail="File type not allowed")

        if not validate_file_size(file.size):
            raise HTTPException(status_code=400, detail="File size exceeds limit")

        # Generate unique file ID
        file_id = str(uuid.uuid4())

        # Create file metadata
        file_metadata = FileMetadata(
            id=file_id,
            original_name=file.filename,
            content_type=file.content_type,
            size=file.size,
            folder=folder,
            uploaded_at=datetime.utcnow()
        )

        # Upload to S3
        s3_key = await s3_service.upload_file(
            file=file,
            file_id=file_id,
            folder=folder
        )

        # Generate CloudFront URL
        cloudfront_url = cloudfront_service.get_file_url(s3_key)

        # Store metadata (in a real app, you'd save to database)
        logger.info(f"File uploaded successfully: {file_id}")

        return FileUploadResponse(
            file_id=file_id,
            filename=file.filename,
            size=file.size,
            content_type=file.content_type,
            s3_key=s3_key,
            cloudfront_url=cloudfront_url,
            uploaded_at=file_metadata.uploaded_at
        )

    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """
    Redirect to CloudFront URL for file download
    """
    try:
        # In a real app, you'd fetch from database
        # For now, we'll construct the S3 key from file_id
        s3_key = f"files/{file_id}"

        # Check if file exists in S3
        if not await s3_service.file_exists(s3_key):
            raise HTTPException(status_code=404, detail="File not found")

        # Generate CloudFront URL
        cloudfront_url = cloudfront_service.get_file_url(s3_key)

        # Redirect to CloudFront
        return RedirectResponse(url=cloudfront_url)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Download failed")


@app.get("/files", response_model=FileListResponse)
async def list_files(
    folder: Optional[str] = Query(None, description="Filter by folder"),
    limit: int = Query(50, ge=1, le=100, description="Number of files to return"),
    offset: int = Query(0, ge=0, description="Number of files to skip")
):
    """
    List files with optional filtering
    """
    try:
        # In a real app, you'd query from database
        # For now, return empty list
        files = []

        return FileListResponse(
            files=files,
            total=len(files),
            limit=limit,
            offset=offset
        )

    except Exception as e:
        logger.error(f"Error listing files: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list files")


@app.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """
    Delete a file from S3
    """
    try:
        # In a real app, you'd fetch from database first
        s3_key = f"files/{file_id}"

        # Check if file exists
        if not await s3_service.file_exists(s3_key):
            raise HTTPException(status_code=404, detail="File not found")

        # Delete from S3
        await s3_service.delete_file(s3_key)

        # In a real app, you'd also delete from database

        logger.info(f"File deleted successfully: {file_id}")
        return {"message": "File deleted successfully", "file_id": file_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Delete failed")


@app.get("/files/{file_id}/metadata")
async def get_file_metadata(file_id: str):
    """
    Get file metadata
    """
    try:
        # In a real app, you'd fetch from database
        s3_key = f"files/{file_id}"

        if not await s3_service.file_exists(s3_key):
            raise HTTPException(status_code=404, detail="File not found")

        # Get metadata from S3
        metadata = await s3_service.get_file_metadata(s3_key)

        return metadata

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metadata for file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get metadata")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
