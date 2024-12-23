import os
import imghdr
from PIL import Image, ImageStat




def check_file_exists(image_path: str, list_images: list) -> tuple[bool, str]:
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
        return True , None
    return False, f"{image_path} It was not included in the list of submitted photos"



def check_file_size(image_path: str, max_size_mb: int, min_size_mb: int) -> tuple[bool, str]:
    """
    Check if the file size of an image is within the allowed size range.

    Args:
        image_path (str): The path to the image file.
        max_size_mb (int): The maximum allowed size for the file in megabytes.
        min_size_mb (int): The minimum allowed size for the file in megabytes.

    Returns:
        tuple[bool, str]: A tuple containing:
            - A boolean indicating whether the file size is within the allowed range.
            - A string message explaining the result or error.
    """
    try:
        # Get the file size in bytes and convert it to megabytes.
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)

        # Check if the file size exceeds the specified maximum size.
        if file_size_mb > max_size_mb:
            return False, f"{image_path} size exceeds {max_size_mb} MB (actual: {file_size_mb:.2f} MB)."

        # Check if the file size is smaller than the specified minimum size.
        if file_size_mb < min_size_mb:
            return False, f"{image_path} size is smaller than the minimum allowed size of {min_size_mb} MB (actual: {file_size_mb:.2f} MB)."

        # If the file size is within the range, return success.
        return True, None

    except Exception as e:
        # Handle any other unexpected exceptions and return the error message.
        return False, f"{image_path} An error occurred: {str(e)}"
    


def check_file_format(image_path : str, allowed_formats : list) -> tuple[bool, str]:
    """
    Check if the file format of the given file is within the allowed formats.

    Args:
        image_path (str): The path to the file to be checked.
        allowed_formats (list): A list of allowed file formats (e.g., ['jpeg', 'png']).

    Returns:
        tuple[bool, str]: A tuple containing:
            - A boolean indicating whether the file format is allowed.
            - A string message explaining the result or error.
    """
    # Determine the actual format of the file using the imghdr module.
    actual_format = imghdr.what(image_path)

    # Check if the actual format is not in the list of allowed formats (case-insensitive).
    if actual_format not in [fmt.lower() for fmt in allowed_formats]:
        # Return False with an error message specifying the invalid format
        # and the list of allowed formats.
        return False, f"{image_path} Invalid format: {actual_format}"
    
    # If the file format is valid, return True with no error message.
    return True, None


def check_image_dimensions(image_path : str, expected_dimensions_list : list) -> tuple[bool, str]:
    """
    Check if the dimensions of the image match any of the expected dimensions from a list.

    Args:
        image_path (str): The path to the image file to be checked.
        expected_dimensions_list (list): A list of tuples, where each tuple represents
                                          an expected (width, height) for the image.

    Returns:
        tuple[bool, str]: A tuple containing:
            - A boolean indicating whether the image dimensions match any of the expected ones.
            - A string message explaining the result or error.
    """
    try:
        # Open the image file using the Image module from PIL (Pillow).
        with Image.open(image_path) as img:
            # Check if the image dimensions match any of the expected dimensions.
            if img.size not in expected_dimensions_list:
                # If dimensions don't match, return False with an error message.
                return False, f"{image_path}Unexpected dimensions: {img.size}."
    
    except Exception as e:
        # Handle any exceptions (e.g., file not found, invalid image format).
        return False, f"{image_path} Error reading image dimensions: {str(e)}"
    
    # Return True if the image dimensions match any of the expected ones.
    return True, None



def check_file_structure(image_path : str) -> tuple[bool, str]:
    """
    Check if the file has a valid header and structure (i.e., if it is a valid image file).

    Args:
        image_path (str): The path to the image file to be checked.

    Returns:
        tuple[bool, str]: A tuple containing:
            - A boolean indicating whether the file has a valid structure.
            - A string message explaining the result or error.
    """
    try:
        # Open the image file using the Image module from PIL (Pillow).
        with Image.open(image_path) as img:
            # Use img.verify() to ensure the file is a valid image and has the correct structure.
            img.verify()  # This checks if the image file is structurally valid.

    except Exception as e:
        # If an exception occurs (e.g., the file is not a valid image or is corrupt),
        # return False with an error message.
        return False, f"{image_path} Invalid  structure or corrupt file: {str(e)}"
    
    # If no exceptions occur, the file structure is valid, so return True with no error message.
    return True, None



def check_pixel_data(image_path : str, expected_mode : str, pixel_range=(0, 255)) -> tuple[bool, str]:
    """
    Check if the pixel data of the image matches the expected properties:
    - The image mode (e.g., RGB, L, etc.)
    - The pixel value range (e.g., 0 to 255 for standard images).

    Args:
        image_path (str): The path to the image file.
        expected_mode (str): The expected image mode (e.g., 'RGB', 'L', etc.).
        pixel_range (tuple): A tuple (min_value, max_value) specifying the allowed pixel value range for the image.

    Returns:
        tuple[bool, str]: A tuple containing:
            - A boolean indicating whether the image's pixel data is valid.
            - A string message explaining the result or error.
    """
    try:
        # Open the image using the Image module from PIL (Pillow).
        with Image.open(image_path) as img:
            # Check if the image mode matches the expected mode (e.g., 'RGB', 'L', etc.).
            if img.mode != expected_mode:
                return False, f"{image_path} Unexpected image mode: {img.mode}. Expected: {expected_mode}."
            
            # Use ImageStat to gather statistics about the image's pixel values.
            stats = ImageStat.Stat(img)
            
            # Get the minimum and maximum pixel values from the image.
            min_pixel = min(stats.extrema[0])  # Get the minimum pixel value (first channel of image).
            max_pixel = max(stats.extrema[0])  # Get the maximum pixel value (first channel of image).
            
            # Check if the pixel values fall within the expected range.
            if min_pixel < pixel_range[0] or max_pixel > pixel_range[1]:
                return False, f"{image_path} Pixel values out of range. Found: ({min_pixel}, {max_pixel}), Expected: {pixel_range}."
    
    except Exception as e:
        # If an exception occurs (e.g., invalid image format, error during analysis),
        # return False with an error message.
        return False, f"{image_path} Error analyzing pixel data: {str(e)}"
    
    # If no errors and the pixel data matches the expected properties, return True.
    return True, None
