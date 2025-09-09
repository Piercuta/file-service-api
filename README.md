# File Service

A FastAPI microservice for file upload, download, and management with S3 and CloudFront integration.

## Features

- **File Upload**: Upload files to S3 with validation
- **File Download**: Download files via CloudFront URLs
- **File Management**: List, delete, and get metadata for files
- **File Validation**: Type and size validation
- **CloudFront Integration**: CDN distribution for better performance
- **Health Checks**: Built-in health monitoring

## API Endpoints

### Health Check
- `GET /health` - Service health status

### File Operations
- `POST /upload` - Upload a file
- `GET /download/{file_id}` - Download a file (redirects to CloudFront)
- `GET /files` - List files with optional filtering
- `DELETE /files/{file_id}` - Delete a file
- `GET /files/{file_id}/metadata` - Get file metadata

## Configuration

Copy `env.example` to `.env` and configure:

```bash
# AWS Configuration
AWS_REGION=us-east-1

# S3 Configuration
S3_BUCKET_NAME=your-file-bucket-name

# CloudFront Configuration
CLOUDFRONT_DOMAIN=your-cloudfront-domain.cloudfront.net
```

## Development

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
cp env.example .env
# Edit .env with your configuration
```

3. Run the service:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

Build and run with Docker:

```bash
# Build image
docker build -t file-service .

# Run container
docker run -p 8000:8000 --env-file .env file-service
```

## Deployment

### Kubernetes

The service is designed to run on EKS. Create a Kubernetes deployment with:

1. ConfigMap for environment variables
2. Secret for AWS credentials
3. Service and Ingress for external access

### Environment Variables

- `AWS_REGION`: AWS region
- `S3_BUCKET_NAME`: S3 bucket name
- `CLOUDFRONT_DOMAIN`: CloudFront distribution domain
- `DEBUG`: Enable debug mode (true/false)
- `MAX_FILE_SIZE`: Maximum file size in bytes (default: 100MB)

## File Types

Supported file types:
- Images: jpg, jpeg, png, gif, bmp, webp, svg
- Documents: pdf, doc, docx, txt, rtf, odt
- Spreadsheets: xls, xlsx, csv, ods
- Presentations: ppt, pptx, odp
- Archives: zip, rar, 7z, tar, gz
- Videos: mp4, avi, mov, wmv, flv, webm
- Audio: mp3, wav, flac, aac, ogg
- Code: py, js, html, css, json, xml, yaml, yml

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

