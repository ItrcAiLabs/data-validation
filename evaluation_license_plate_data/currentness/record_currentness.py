import os
import json
import time

def RecordCurrentness(photo_folder: str, threshold_days: float) -> dict:
    """
    Evaluates record currentness for a folder of photo files and gathers summary information.
    
    For each photo in the folder (files ending with .jpg, .jpeg, .png), the function:
      - Computes the file age in days (using the file modification time).
      - Marks the file as current (record_currentness = 1) if its age is <= threshold_days;
        otherwise, it is considered out-of-date (record_currentness = 0).
    
    Returns a dictionary containing, for each file:
      - "age_days": The file’s age in days.
      - "record_currentness": 1 if the file is current, or 0 if not.
    
    The summary includes:
      - total_files: Total number of image files processed.
      - current_files: Number of files considered current.
      - overall_currentness: Ratio (current_files / total_files).
    
    Parameters:
      photo_folder: Path to the folder containing photo files.
      threshold_days: The age threshold in days; files with age <= threshold_days are considered current.
    
    Returns:
      A dictionary with detailed file results and a summary.
    """
    details = {}
    total_files = 0
    current_files = 0

    # Current time in seconds since epoch.
    now = time.time()

    for filename in os.listdir(photo_folder):
        # Check for common image formats.
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            total_files += 1
            file_path = os.path.join(photo_folder, filename)
            
            # Use the file modification time.
            mtime = os.path.getmtime(file_path)
            age_seconds = now - mtime
            age_days = age_seconds / 86400.0  # Convert seconds to days.
            is_current = age_days <= threshold_days
            
            # Instead of boolean, store 1 (if current) or 0 (if not current)
            details[filename] = {
                "age_days": age_days,
                "record_currentness": 1 if is_current else 0
            }
            
            if is_current:
                current_files += 1

    overall_currentness = current_files / total_files if total_files > 0 else 0

    summary = {
        "overall_record_currentness": overall_currentness
    }

    result =  {"files": details, "summary": summary}
    return json.dumps(result, ensure_ascii=False, indent=4)


# # --- Example Usage ---
# photo_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"

# threshold_days = 30  # A file is considered current if it is 30 days old or less.

# currentness_report = RecordCurrentness(photo_folder, threshold_days)
# print(currentness_report)


#out put

  # {
  #     "files": {
  #         "1000423.png": {
  #             "age_days": 1383.8719464692033,
  #             "record_currentness": 0
  #         },
  #         "1000211.png": {
  #             "age_days": 1383.8725714692032,
  #             "record_currentness": 0
  #         },
  #         "1000212.png": {
  #             "age_days": 1383.872548321055,
  #             "record_currentness": 0
  #         },
  #         "1000395.png": {
  #             "age_days": 1383.872062209944,
  #             "record_currentness": 0
  #         },
  #         "1000396.png": {
  #             "age_days": 1383.872062209944,
  #             "record_currentness": 0
  #         },
  #         "1000244.png": {
  #             "age_days": 1383.8724788766106,
  #             "record_currentness": 0
  #         },
  #         "1000229.png": {
  #             "age_days": 1383.8725020247587,
  #             "record_currentness": 0
  #         },
  #         "1000393.png": {
  #             "age_days": 1383.872062209944,
  #             "record_currentness": 0
  #         },
  #         "1000198.png": {
  #             "age_days": 1383.872687209944,
  #             "record_currentness": 0
  #         },
  #         "1000376.png": {
  #             "age_days": 1383.8721085062402,
  #             "record_currentness": 0
  #         }
  #     },
  #     "summary": {
  #         "overall_record_currentness": 0.0
  #     }
  # }