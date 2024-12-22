import os
import imghdr
from PIL import Image, ImageStat




def check_file_exists(image_path: str, list_images: list) -> bool:
    """
    Check if the file name (without extension) exists in the provided list of image names.

    :param path_image: The full path of the image file (string)
    :param list_images: A list of image names (strings) to check against
    :return: Boolean value indicating whether the image name (without extension) is in the list
    """
    # Extract the name of the file without the extension
    name = os.path.splitext(os.path.basename(image_path))[0]

    # Check if the extracted file name exists in the list of image names
    if name in list_images:
        return True
    return False



def check_file_size(image_path: str, max_size_mb: int, min_size_mb: int):
    """Check if the file size is within the allowed size range."""
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
    
    # Check if the file size exceeds the maximum size
    if file_size_mb > max_size_mb:
        return False, f"File size exceeds {max_size_mb} MB (actual: {file_size_mb:.2f} MB)."
    
    # Check if the file size is smaller than the minimum size
    if file_size_mb < min_size_mb:
        return False, f"File size is smaller than the minimum allowed size of {min_size_mb} MB (actual: {file_size_mb:.2f} MB)."
    
    return True, None

