from PIL import Image
import os
import json

class DataModelAccuracyIMG:
    def __init__(self, folder_path: str, required_metadata: list) -> None:
        """
        Validates if required metadata fields exist in multiple image files.

        Parameters:
        - folder_path: Path to the folder containing image files.
        - required_metadata: List of required metadata keys.
          Example: ["width", "height", "format"]
        """
        self.folder_path = folder_path
        self.required_metadata = required_metadata
        self.results = {}

    def validate_images(self) -> None:
        """
        Processes all image files in the folder and checks for missing metadata.
        """
        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):  # Process only image files
                file_path = os.path.join(self.folder_path, filename)
                self.results[filename] = self.validate_image(file_path)

    def validate_image(self, file_path: str) -> dict:
        """
        Checks an image file for required metadata fields.

        Returns:
        - Dictionary containing missing fields and accuracy score.
        """
        missing_metadata = []
        try:
            with Image.open(file_path) as img:
                metadata = {
                    "width": img.width,
                    "height": img.height,
                    "format": img.format
                }

                # Check if required metadata fields exist
                for field in self.required_metadata:
                    if metadata.get(field) is None:
                        missing_metadata.append(field)

                accuracy = 1 - (len(missing_metadata) / len(self.required_metadata))
                return {"accuracy": accuracy, "missing_metadata": missing_metadata}

        except Exception as e:
            return {"error": str(e), "accuracy": 0.0, "missing_metadata": []}

    def get_model_accuracy(self) -> str:
        """
        Generates a JSON report summarizing the validation results.

        Returns:
        - JSON string summarizing accuracy and missing metadata for all images.
        """
        overall_accuracy = (
            sum(file["accuracy"] for file in self.results.values() if "accuracy" in file) / len(self.results)
            if self.results else 0
        )
        
        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)


# # Define required metadata fields
# required_metadata = ["width", "height", "format"]

# # Specify folder path containing image files
# folder_path = "/home/reza/Desktop/data-validation/img/Plate/img"  # Change this to your folder path

# # Run validation on all images in the folder
# validator = DataModelAccuracyIMG(folder_path, required_metadata)
# validator.validate_images()
# print(validator.get_model_accuracy())

#output
# {
#     "1000423.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000211.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000212.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000395.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000396.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000244.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000229.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000393.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000198.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "1000376.png": {
#         "accuracy": 1.0,
#         "missing_metadata": []
#     },
#     "summary": {
#         "overall_accuracy": 1.0
#     }
# }