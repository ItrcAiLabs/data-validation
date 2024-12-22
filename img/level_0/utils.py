import os
import imghdr
from PIL import Image, ImageStat

import os
import json

import os

def check_file_exists(path_image: str, list_images: list) -> bool:
    """
    Check if the file name (without extension) exists in the provided list of image names.

    :param path_image: The full path of the image file (string)
    :param list_images: A list of image names (strings) to check against
    :return: Boolean value indicating whether the image name (without extension) is in the list
    """
    # Extract the name of the file without the extension
    name = os.path.splitext(os.path.basename(path_image))[0]

    # Check if the extracted file name exists in the list of image names
    if name in list_images:
        return True
    return False
