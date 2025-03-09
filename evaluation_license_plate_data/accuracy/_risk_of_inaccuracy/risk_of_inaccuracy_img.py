import os
import json
from PIL import Image

class RiskOfInaccuracyImg:
    def __init__(self, image_folder: str, allowed_file_types: list = None,
                 dimension_range: dict = None, file_size_range: dict = None) -> None:
        """
        Validate images by checking file type, dimensions, and file size.
        
        Parameters:
            image_folder: Path to the folder containing image files.
            allowed_file_types: List of allowed file extensions (without the dot). Defaults: ['png', 'jpg', 'jpeg'].
            dimension_range: Dictionary with keys min_width, max_width, min_height, max_height.
                Example: {'min_width': 800, 'max_width': 1920, 'min_height': 600, 'max_height': 1080}.
            file_size_range: Dictionary with keys min_size, max_size (in bytes).
                Example: {'min_size': 1024, 'max_size': 5000000}.
        """
        self.image_folder = image_folder
        self.results = {}
        self.allowed_file_types = allowed_file_types if allowed_file_types is not None else ['png', 'jpg', 'jpeg']
        self.dimension_range = dimension_range if dimension_range is not None else {
            'min_width': 0,
            'max_width': float('inf'),
            'min_height': 0,
            'max_height': float('inf')
        }
        self.file_size_range = file_size_range if file_size_range is not None else {
            'min_size': 0,
            'max_size': float('inf')
        }

    def validate_files(self) -> None:
        """
        Process all image files in the specified folder and validate their file type, dimensions, and file size.
        For each file, compute a score and error message for each field as well as the overall file accuracy.
        """
        for filename in os.listdir(self.image_folder):
            file_path = os.path.join(self.image_folder, filename)
            if os.path.isfile(file_path):
                self.results[filename] = self.validate_image(file_path)

    def validate_image(self, file_path: str) -> dict:
        """
        Validate a single image file.
        
        Checks:
          - File type: The file extension must be in the allowed_file_types list.
          - Dimensions: The image's width and height must fall within the specified dimension_range.
          - File size: The file size (in bytes) must be within the specified file_size_range.
          
        Returns a dictionary containing:
          - fields: { file_type, dimensions, file_size }
          - errors: Error messages in case any issue is found.
          - file_accuracy: The average score of the validated fields.
        """
        field_scores = {}
        field_errors = {}
        total_fields = 3  # file_type, dimensions, file_size
        
        # Validate file type
        ext = os.path.splitext(file_path)[1].lower().replace('.', '')
        if ext in [ft.lower() for ft in self.allowed_file_types]:
            field_scores["file_type"] = 1
            field_errors["file_type"] = ""
        else:
            field_scores["file_type"] = 0
            field_errors["file_type"] = f"Invalid file type '{ext}'. Allowed types: {self.allowed_file_types}."
        
        # Validate image dimensions
        try:
            with Image.open(file_path) as img:
                width, height = img.size
                if (self.dimension_range['min_width'] <= width <= self.dimension_range['max_width'] and
                    self.dimension_range['min_height'] <= height <= self.dimension_range['max_height']):
                    field_scores["dimensions"] = 1
                    field_errors["dimensions"] = ""
                else:
                    field_scores["dimensions"] = 0
                    field_errors["dimensions"] = (
                        f"Image dimensions {width}x{height} are out of the allowed range: "
                        f"width [{self.dimension_range['min_width']}, {self.dimension_range['max_width']}], "
                        f"height [{self.dimension_range['min_height']}, {self.dimension_range['max_height']}]."
                    )
        except Exception as e:
            field_scores["dimensions"] = 0
            field_errors["dimensions"] = f"Error opening image: {e}"
        
        # Validate file size
        try:
            size_bytes = os.path.getsize(file_path)
            if self.file_size_range['min_size'] <= size_bytes <= self.file_size_range['max_size']:
                field_scores["file_size"] = 1
                field_errors["file_size"] = ""
            else:
                field_scores["file_size"] = 0
                field_errors["file_size"] = (
                    f"File size {size_bytes} bytes is out of the allowed range: "
                    f"[{self.file_size_range['min_size']}, {self.file_size_range['max_size']}]."
                )
        except Exception as e:
            field_scores["file_size"] = 0
            field_errors["file_size"] = f"Error obtaining file size: {e}"
        
        file_accuracy = sum(field_scores.values()) / total_fields
        # Remove empty error messages
        field_errors = {key: value for key, value in field_errors.items() if value != ""}
        
        return {"fields": field_scores, "errors": field_errors, "file_accuracy": file_accuracy}

    def get_risk_inaccuracy(self) -> str:
        """
        Generate a JSON report that includes for each image file:
          - The score for each field,
          - Error messages (if any) for each field,
          - The overall file accuracy (file_accuracy)
        Finally, an overall accuracy (overall_accuracy) is computed as the average accuracy of all files.
        """
        valid_file_results = [
            file_data 
            for key, file_data in self.results.items() 
            if key != "summary" and isinstance(file_data, dict)
        ]
        total_files = len(valid_file_results)
        overall_accuracy = 0
        if total_files > 0:
            overall_accuracy = sum(file_data["file_accuracy"] for file_data in valid_file_results) / total_files
        
        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)


# --- Example Usage ---
# Specify the image folder path.
# image_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img" 

# allowed_file_types = ['png']  # Only PNG images are allowed.
# dimension_range = {
#     'min_width': 800,
#     'max_width': 1920,
#     'min_height': 600,
#     'max_height': 1080
# }
# file_size_range = {
#     'min_size': 1024,      # Minimum 1 KB
#     'max_size': 5_000_000    # Maximum 5 MB
# }

# validator = RiskOfInaccuracyImg(image_folder, allowed_file_types, dimension_range, file_size_range)
# validator.validate_files()
# print(validator.get_risk_inaccuracy())


#output

# {
#     "1000423.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000211.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000212.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000395.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000396.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000244.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000229.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000393.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000198.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "1000376.png": {
#         "fields": {
#             "file_type": 1,
#             "dimensions": 0,
#             "file_size": 1
#         },
#         "errors": {
#             "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."
#         },
#         "file_accuracy": 0.6666666666666666
#     },
#     "summary": {
#         "overall_accuracy": 0.6666666666666666
#     }
# }