import os
from PIL import Image

def check_file_exists(file_path):
    """Check if the file exists."""
    if not os.path.exists(file_path):
        return False, "File does not exist."
    return True, None

def check_file_size(file_path, max_size_mb):
    """Check if the file size is within the allowed limit."""
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if file_size_mb > max_size_mb:
        return False, f"File size exceeds {max_size_mb} MB (actual: {file_size_mb:.2f} MB)."
    return True, None

def check_file_format(file_path, allowed_formats):
    """Check if the file format is in the allowed formats."""
    try:
        with Image.open(file_path) as img:
            file_format = img.format
            if file_format not in allowed_formats:
                return False, f"Invalid file format: {file_format}. Allowed formats: {allowed_formats}."
    except Exception as e:
        return False, f"Error reading image: {str(e)}"
    return True, None

def check_image_dimensions(file_path, expected_dimensions):
    """Check if the image dimensions match the expected dimensions."""
    try:
        with Image.open(file_path) as img:
            if img.size != expected_dimensions:
                return False, f"Unexpected dimensions: {img.size}. Expected: {expected_dimensions}."
    except Exception as e:
        return False, f"Error reading image dimensions: {str(e)}"
    return True, None