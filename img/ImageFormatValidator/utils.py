import os
import imghdr
from PIL import Image, ImageStat

def check_file_exists(image_path: str, list_images: list) -> tuple[bool, str]:
    """
    Check if the file name (without extension) exists in the provided list of image names.
    """
    name = os.path.basename(image_path)
    if name in list_images:
        return True, "File exists in the list of images"
    return False, "It was not included in the list of submitted photos"

def check_file_size(image_path: str, max_size_mb: int, min_size_mb: int) -> tuple[bool, str]:
    """
    Check if the file size of an image is within the allowed size range.
    """
    try:
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

        if file_size_mb > max_size_mb:
            return False, f"File size exceeds {max_size_mb} MB (actual: {file_size_mb:.2f} MB)."
        if file_size_mb < min_size_mb:
            return False, f"File size is smaller than the minimum allowed size of {min_size_mb} MB (actual: {file_size_mb:.2f} MB)."
        return True, "File size is within the allowed range."
    
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def check_file_format(image_path : str, allowed_formats : list) -> tuple[bool, str]:
    """
    Check if the file format of the given file is within the allowed formats.
    """
    actual_format = imghdr.what(image_path)
    if actual_format not in [fmt.lower() for fmt in allowed_formats]:
        return False, f"Invalid format: {actual_format}. Allowed formats are: {', '.join(allowed_formats)}."
    
    return True, "File format is valid."

def check_image_dimensions(image_path : str, expected_dimensions_list : list) -> tuple[bool, str]:
    """
    Check if the dimensions of the image match any of the expected dimensions from a list.
    """
    try:
        with Image.open(image_path) as img:
            if img.size not in expected_dimensions_list:
                return False, f"Unexpected dimensions: {img.size}. Expected one of {expected_dimensions_list}."
    
    except Exception as e:
        return False, f"Error reading image dimensions: {str(e)}"
    
    return True, "Image dimensions match the expected values."

def check_file_structure(image_path : str) -> tuple[bool, str]:
    """
    Check if the file has a valid header and structure (i.e., if it is a valid image file).
    """
    try:
        with Image.open(image_path) as img:
            img.verify()  # This checks if the image file is structurally valid.
    except Exception as e:
        return False, f"Invalid structure or corrupt file: {str(e)}"
    
    return True, "File structure is valid."

def check_pixel_data(image_path : str, expected_mode : str, pixel_range=(0, 255)) -> tuple[bool, str]:
    """
    Check if the pixel data of the image matches the expected properties.
    """
    try:
        with Image.open(image_path) as img:
            if img.mode != expected_mode:
                return False, f"Unexpected image mode: {img.mode}. Expected: {expected_mode}."
            
            stats = ImageStat.Stat(img)
            min_pixel = min(stats.extrema[0])
            max_pixel = max(stats.extrema[0])
            
            if min_pixel < pixel_range[0] or max_pixel > pixel_range[1]:
                return False, f"Pixel values out of range. Found: ({min_pixel}, {max_pixel}), Expected: {pixel_range}."
    
    except Exception as e:
        return False, f"Error analyzing pixel data: {str(e)}"
    
    return True, "Pixel data is valid."




