"""
File validation utilities
"""

import os
from typing import Optional

# Allowed file types (extensions)
ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
    'spreadsheet': ['.xls', '.xlsx', '.csv', '.ods'],
    'presentation': ['.ppt', '.pptx', '.odp'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'code': ['.py', '.js', '.html', '.css', '.json', '.xml', '.yaml', '.yml']
}

# Maximum file size (in bytes) - 100MB
MAX_FILE_SIZE = 100 * 1024 * 1024


def validate_file_type(filename: Optional[str]) -> bool:
    """
    Validate file type based on extension

    Args:
        filename: Name of the file to validate

    Returns:
        True if file type is allowed, False otherwise
    """
    if not filename:
        return False

    # Get file extension
    _, ext = os.path.splitext(filename.lower())

    # Check if extension is in any allowed category
    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return True

    return False


def validate_file_size(file_size: Optional[int]) -> bool:
    """
    Validate file size

    Args:
        file_size: Size of the file in bytes

    Returns:
        True if file size is within limits, False otherwise
    """
    if file_size is None:
        return False

    return file_size <= MAX_FILE_SIZE


def get_file_category(filename: str) -> Optional[str]:
    """
    Get file category based on extension

    Args:
        filename: Name of the file

    Returns:
        Category name or None if not found
    """
    if not filename:
        return None

    _, ext = os.path.splitext(filename.lower())

    for category, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return category

    return None


def is_image_file(filename: str) -> bool:
    """
    Check if file is an image

    Args:
        filename: Name of the file

    Returns:
        True if file is an image, False otherwise
    """
    return get_file_category(filename) == 'image'


def is_document_file(filename: str) -> bool:
    """
    Check if file is a document

    Args:
        filename: Name of the file

    Returns:
        True if file is a document, False otherwise
    """
    return get_file_category(filename) == 'document'

