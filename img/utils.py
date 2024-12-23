import os  # Importing the standard 'os' library to work with file paths and directories.

def list_all_files(directory : str) -> list:
    """
    This function lists all the files in a given folder and its subfolders.
    
    Parameters:
        directory (str): The path of the folder to search for files.
    
    Returns:
        file_paths (list): A list of absolute paths for all files in the folder and subfolders.
    """
    file_paths = []  # Create an empty list to store the file paths.

    # os.walk traverses the directory tree recursively.
    for root, dirs, files in os.walk(directory):
        # root: The current folder being processed.
        # dirs: A list of subdirectories in the current folder.
        # files: A list of files in the current folder.

        for file in files:  # Iterate over all files in the current folder.
            # Construct the full file path using os.path.join.
            file_paths.append(os.path.join(root, file))
    
    return file_paths  # Return the list of full file paths.