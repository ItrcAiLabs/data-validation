import os
import json
from PIL import Image

def DataFormatConsistencyImg(img_path):
    extension_to_format = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.gif': 'GIF',
        '.bmp': 'BMP'
    }

    # Get list of files with recognized image extensions
    files = [
        f for f in os.listdir(img_path)
        if os.path.isfile(os.path.join(img_path, f)) and
           os.path.splitext(f)[1].lower() in extension_to_format
    ]

    # Initialize report structure
    report = {"files": {}, "summary": {}}
    scores = []

    # Process each file
    for filename in files:
        # Get the extension and expected format
        ext = os.path.splitext(filename)[1].lower()
        expected_format = extension_to_format[ext]

        # Determine the actual format
        try:
            img = Image.open(os.path.join(img_path, filename))
            actual_format = img.format if img.format else 'Unknown'
        except Exception:
            actual_format = 'Unknown'

        # Check if formats match
        format_consistency = 1 if actual_format == expected_format else 0

        # Build file report based on consistency
        if format_consistency == 1:
            file_report = {
                'format_consistency': 1,
                "errors" : ""
            }
        else:
            error_message = (
                'File is not a valid image.' if actual_format == 'Unknown'
                else f'Expected {expected_format} but found {actual_format}.'
            )
            file_report = {
                'format_consistency': 0,
                'errors': error_message
            }

        # Add to report and collect score
        report["files"][filename] = file_report
        scores.append(format_consistency)

    # Calculate summary statistics
    overall_consistency = sum(scores) / len(scores) if scores else 0.0
    report["summary"]["data_format_consistency"] = overall_consistency

    return json.dumps(report, ensure_ascii=False, indent=4)

