from PIL import Image
from PIL.ExifTags import TAGS
import os
import json

class DataModelAccuracyIMG:
    def __init__(self, folder_path: str, required_metadata: list) -> None:
        """
        Validates if required metadata fields exist in multiple image files.

        Parameters:
          - folder_path: Path to the folder containing image files.
          - required_metadata: List of required metadata keys.
            Example: ["width", "height", "format", "location", "date"]
        """
        self.folder_path = folder_path
        self.required_metadata = required_metadata
        self.results = {}

    def validate_images(self) -> None:
        """
        Processes all image files in the folder and checks for missing metadata.
        """
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(self.folder_path, filename)
                self.results[filename] = self.validate_image(file_path)

    def validate_image(self, file_path: str) -> dict:
        """
        Checks an image file for required metadata fields.

        Returns a dictionary with:
          - "fields": individual field scores (1.0 if present, 0.0 if missing),
          - "acc": overall accuracy (average of field scores),
          - "missing_metadata": list of missing required metadata fields.
        """
        missing_metadata = []
        field_scores = {}
        metadata = {}

        try:
            with Image.open(file_path) as img:
                # Basic metadata from PIL
                metadata["width"] = img.width
                metadata["height"] = img.height
                metadata["format"] = img.format

                # Try to extract EXIF data for additional metadata
                exif_data = img._getexif()
                if exif_data:
                    exif = {TAGS.get(key, key): value for key, value in exif_data.items()}
                    # For location, check if 'GPSInfo' exists in EXIF; if present, store it
                    if "GPSInfo" in exif:
                        metadata["location"] = exif["GPSInfo"]
                    # For date, check if 'DateTime' exists in EXIF
                    if "DateTime" in exif:
                        metadata["date"] = exif["DateTime"]
        except Exception as e:
            return {"error": str(e), "fields": {}, "acc": 0.0, "missing_metadata": []}

        # Check each required metadata field and assign score 1 if exists, 0 if missing.
        for field in self.required_metadata:
            # We consider a field "present" if it exists and is not None.
            if metadata.get(field) is not None:
                field_scores[f"{field}_accuracy"] = 1.0
            else:
                field_scores[f"{field}_accuracy"] = 0.0
                missing_metadata.append(field)

        overall_accuracy = sum(field_scores.values()) / len(self.required_metadata) if self.required_metadata else 0

        return {
            "fields": field_scores,
            "file_accuracy": overall_accuracy,
            "missing_metadata": missing_metadata
        }

    def get_model_accuracy(self) -> str:
        """
        Generates a JSON report summarizing the validation results for all images.
        Also computes an overall average accuracy across all files.

        Returns a JSON string of the report.
        """
        valid_files = [res for key, res in self.results.items() if key != "summary" and "file_accuracy" in res]
        overall_accuracy = 0
        if valid_files:
            overall_accuracy = sum(res["file_accuracy"] for res in valid_files) / len(valid_files)
        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)

# --- Example Usage ---
# required_metadata = ["width", "height", "format", "location", "date"]
# folder_path = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"  # Change to your folder path

# validator = DataModelAccuracyIMG(folder_path, required_metadata)
# validator.validate_images()
# report = validator.get_model_accuracy()
# print(report)




#output

    # {
    #     "1000423.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000211.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000212.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000395.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000396.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000244.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000229.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000393.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000198.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "1000376.png": {
    #         "fields": {
    #             "width_accuracy": 1.0,
    #             "height_accuracy": 1.0,
    #             "format_accuracy": 1.0,
    #             "location_accuracy": 0.0,
    #             "date_accuracy": 0.0
    #         },
    #         "file_accuracy": 0.6,
    #         "missing_metadata": [
    #             "location",
    #             "date"
    #         ]
    #     },
    #     "summary": {
    #         "overall_accuracy": 0.6
    #     }
    # }