"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import os
import json
import xml.etree.ElementTree as ET

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
            if filename.endswith(".xml"):
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    xml_content = file.read()
                    self.results[filename] = self.validate_structure(xml_content)

    def validate_structure(self, xml_content: str) -> dict:
        """
        Checks an XML file for required fields and calculates accuracy.
        
        For each required field, if it exists the score is 1, otherwise 0.
        The overall accuracy ("acc") is the average of the field scores.

        Returns a dictionary with:
          - "fields": individual field scores,
          - "acc": overall accuracy,
          - "missing_fields": list of missing required fields.
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return {
                "error": "Invalid XML format", 
                "fields": {}, 
                "file_accuracy": 0.0, 
                "missing_fields": []
            }
        
        field_scores = {}
        missing_fields = []
        for field in self.required_fields:
            # Split the field path and check for its existence
            field_path = field.split('/')
            exists = self._check_element(root, field_path)
            key = self._field_key(field)
            if exists:
                field_scores[key] = 1.0
            else:
                field_scores[key] = 0.0
                missing_fields.append(field)
        
        overall_accuracy = sum(field_scores.values()) / len(self.required_fields) if self.required_fields else 0
        
        return {
            "fields": field_scores,
            "file_accuracy": overall_accuracy,
            "missing_fields": missing_fields
        }

    def _check_element(self, parent, elements: list) -> bool:
        """
        Recursively checks for the presence of elements in the XML structure without
        modifying the original list.
        """
        if not elements:
            return True
        current_element = elements[0]
        found = parent.find(current_element)
        if found is None:
            return False
        return self._check_element(found, elements[1:])

    def _field_key(self, field: str) -> str:
        """
        Converts a required field path into a key name for the results.
        For example, "LicensePlate/RegistrationPrefix" becomes "registrationprefix_accuracy".
        """
        key = field.replace("/", "").lower()
        return f"{key}_accuracy"

    def get_model_accuracy(self) -> str:
        """
        Generates a JSON report summarizing the validation results for each file.
        Also, computes an overall average accuracy across all files.

        Returns:
          A JSON string of the report.
        """
        valid_files = [
            res for key, res in self.results.items()
            if key != "overall_accuracy" and "file_accuracy" in res
        ]
        overall_accuracy = 0
        if valid_files:
            overall_accuracy = sum(res["file_accuracy"] for res in valid_files) / len(valid_files)
        self.results["overall_accuracy"] = overall_accuracy
        return json.dumps(self.results, ensure_ascii=False, indent=4)



# Define required fields based on expected structure
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
# folder_path = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"  # Change this to your folder path

# # Run validation on all XML files in the folder
# validator = DataModelAccuracyXML(folder_path, required_fields)
# validator.validate_files()
# print(validator.get_model_accuracy())


# output
    # {
    #     "1000423.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000393.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000376.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000396.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000395.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000212.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000229.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000244.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000211.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000198.xml": {
    #         "fields": {
    #             "cardatalicenseplateregistrationprefix_accuracy": 0.0,
    #             "licenseplateseriesletter_accuracy": 1.0,
    #             "licenseplateregistrationnumber_accuracy": 1.0,
    #             "licenseplateprovincecode_accuracy": 1.0,
    #             "carmodel_accuracy": 1.0,
    #             "carcolor_accuracy": 1.0,
    #             "licenseplatecoordinatesx_accuracy": 1.0,
    #             "licenseplatecoordinatesy_accuracy": 1.0,
    #             "licenseplatecoordinateswidth_accuracy": 1.0,
    #             "licenseplatecoordinatesheight_accuracy": 1.0,
    #             "carcoordinatesx_accuracy": 1.0,
    #             "carcoordinatesy_accuracy": 1.0,
    #             "carcoordinateswidth_accuracy": 1.0,
    #             "carcoordinatesheight_accuracy": 1.0
    #         },
    #         "file_accuracy": 0.9285714285714286,
    #         "missing_fields": [
    #             "CarData/LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "overall_accuracy": 0.9285714285714286
    # }