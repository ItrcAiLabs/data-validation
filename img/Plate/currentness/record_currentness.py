import os
import json
import time

def RecordCurrentness(photo_folder: str, threshold_days: float) -> dict:
    """
    Evaluates record currentness for a folder of photo files and gathers a list of photo formats.
    
    For each photo in the folder (files ending with .jpg, .jpeg, .png), the function:
      - Computes the file age in days (using the file modification time).
      - Marks the file as current (record_currentness = True) if its age is <= threshold_days;
        otherwise, it is considered out-of-date (record_currentness = False).
      - Collects the file extension (format) for a summary.
    
    Returns a dictionary containing, for each file:
      - "age_days": The file’s age in days.
      - "record_currentness": Boolean indicating if the file is current.
    
    The summary includes:
      - total_files: Total number of image files processed.
      - current_files: Number of files considered current.
      - overall_currentness: Ratio (current_files/total_files).
      - formats: A dictionary of file formats (extensions) and their counts.
    
    Parameters:
      photo_folder: Path to the folder containing photo files.
      threshold_days: The age threshold in days; files with age <= threshold_days are current.
    
    Returns:
      A dictionary with detailed file results and a summary.
    """
    results = {}
    total_files = 0
    current_files = 0
    formats = {}
    details = {}

    # Current time in seconds since epoch.
    now = time.time()

    for filename in os.listdir(photo_folder):
        # Check for common image formats.
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            total_files += 1
            file_path = os.path.join(photo_folder, filename)
            
            # Update the formats dictionary (use lower-case extension without the dot).
            ext = os.path.splitext(filename)[1].lower().lstrip('.')
            formats[ext] = formats.get(ext, 0) + 1

            # Use the file modification time.
            mtime = os.path.getmtime(file_path)
            age_seconds = now - mtime
            age_days = age_seconds / 86400.0  # Convert seconds to days.
            is_current = age_days <= threshold_days
            if is_current:
                current_files += 1
            
            details[filename] = {
                "age_days": age_days,
                "record_currentness": is_current,
                "format": ext
            }

    overall_currentness = current_files / total_files if total_files > 0 else 0

    summary = {
        "overall_currentness": overall_currentness,
    }

    return {"files": details, "summary": summary}

# photo_folder = "/home/reza/Desktop/data-validation/img/Plate/assets/img"
# threshold_days = 30  # For example, a file is considered current if it is 30 days old or less.

# currentness_report = RecordCurrentness(photo_folder, threshold_days)
# print(json.dumps(currentness_report, ensure_ascii=False, indent=4))


#output 

    # {
    #     "files": {
    #         "1000423.png": {
    #             "age_days": 1382.6363701190523,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000211.png": {
    #             "age_days": 1382.6369951190522,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000212.png": {
    #             "age_days": 1382.6369719709041,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000395.png": {
    #             "age_days": 1382.636485859793,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000396.png": {
    #             "age_days": 1382.636485859793,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000244.png": {
    #             "age_days": 1382.6369025264598,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000229.png": {
    #             "age_days": 1382.636925674608,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000393.png": {
    #             "age_days": 1382.636485859793,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000198.png": {
    #             "age_days": 1382.637110859793,
    #             "record_currentness": false,
    #             "format": "png"
    #         },
    #         "1000376.png": {
    #             "age_days": 1382.6365321560893,
    #             "record_currentness": false,
    #             "format": "png"
    #         }
    #     },
    #     "summary": {
    #         "overall_currentness": 0.0
    #     }
    # }