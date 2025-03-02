"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import xml.etree.ElementTree as ET
import json
import os

class DataModelAccuracyXML:
    def __init__(self, folder_path: str, required_fields: list) -> None:
        """
        Validates the structure of multiple XML files in a folder.

        Parameters:
        - folder_path: Path to the folder containing XML files.
        - required_fields: List of required XML tags in a hierarchical format.
        """
        self.folder_path = folder_path
        self.required_fields = required_fields
        self.results = {}

    def validate_files(self) -> None:
        """
        Processes all XML files in the folder and checks for missing fields.
        """
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".xml"):  # Only process XML files
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    xml_content = file.read()
                    self.results[filename] = self.validate_structure(xml_content)

    def validate_structure(self, xml_content: str) -> dict:
        """
        Checks an XML file for required fields and calculates accuracy.

        Returns:
        - Dictionary containing missing fields and accuracy score.
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return {"error": "Invalid XML format", "accuracy": 0.0, "missing_fields": []}

        missing_fields = [field for field in self.required_fields if not self._check_element(root, field.split('/'))]

        accuracy = 1 - (len(missing_fields) / len(self.required_fields))
        return {"accuracy": accuracy, "missing_fields": missing_fields}

    def _check_element(self, parent, elements):
        """
        Recursively checks for the presence of elements in the XML structure.
        """
        if not elements:
            return True
        current_element = elements.pop(0)
        found = parent.find(current_element)
        return found is not None and self._check_element(found, elements)

    def get_model_accuracy(self) -> str:
        """
        Generates a JSON report summarizing the validation results.

        Returns:
        - JSON string summarizing accuracy and missing fields for all files.
        """
        overall_accuracy = sum(file["accuracy"] for file in self.results.values()) / len(self.results) if self.results else 0
        self.results["overall_accuracy"] = overall_accuracy
        return json.dumps(self.results, ensure_ascii=False, indent=4)


# # Define required fields based on expected structure
# required_fields = [
#     "CarData/LicensePlate/RegistrationPrefix",
#     "LicensePlate/SeriesLetter",
#     "LicensePlate/RegistrationNumber",
#     "LicensePlate/ProvinceCode",
#     "CarModel",
#     "CarColor",
#     "LicensePlateCoordinates/X",
#     "LicensePlateCoordinates/Y",
#     "LicensePlateCoordinates/Width",
#     "LicensePlateCoordinates/Height",
#     "CarCoordinates/X",
#     "CarCoordinates/Y",
#     "CarCoordinates/Width",
#     "CarCoordinates/Height"
# ]

# # Specify folder path containing XML files
# folder_path = "/home/reza/Desktop/data-validation/img/Plate/xml"  # Change this to your folder path

# # Run validation on all XML files in the folder
# validator = DataModelAccuracyXML(folder_path, required_fields)
# validator.validate_files()
# print(validator.get_model_accuracy())


# output
# {
#     "1000423.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000393.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000376.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000396.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000395.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000212.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000229.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000244.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000211.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "1000198.xml": {
#         "accuracy": 0.9285714285714286,
#         "missing_fields": [
#             "CarData/LicensePlate/RegistrationPrefix"
#         ]
#     },
#     "overall_accuracy": 0.9285714285714286
# }