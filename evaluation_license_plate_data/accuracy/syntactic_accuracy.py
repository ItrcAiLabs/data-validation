import os
import re
import json
import xml.etree.ElementTree as ET

class SyntacticAccuracy:
    def __init__(self, xml_folder: str, xpaths: dict) -> None:
        """
        Initializes the evaluator with the folder containing XML files and the XML paths
        for the required fields.

        Parameters:
            xml_folder: Path to the folder containing XML files.
            xpaths: Dictionary mapping field names to their XPath locations.
                    Expected keys:
                      - "registration_prefix": e.g. "LicensePlate/RegistrationPrefix"
                      - "series_letter": e.g. "LicensePlate/SeriesLetter"
                      - "registration_number": e.g. "LicensePlate/RegistrationNumber"
                      - "province_code": e.g. "LicensePlate/ProvinceCode"
        """
        self.xml_folder = xml_folder
        self.xpaths = xpaths
        self.results = {}

    def compute_accuracy(self, xml_content: str) -> dict:
        """
        Computes the syntactic accuracy for Iranian vehicle license plate components
        based on an XML string.

        Checks:
          - RegistrationPrefix must match exactly 2 digits.
          - SeriesLetter must consist solely of English letters (A-Z or a-z).
          - RegistrationNumber must match exactly 3 digits.
          - ProvinceCode must match 1 or 2 digits.

        For each field:
          - If valid, a score of 1.0 is given.
          - If invalid, a score of 0.0 is given and an error message is recorded.

        The overall syntactic accuracy is computed as the average of the component scores.
        The overall accuracy is stored under the key "acc", and individual field accuracies
        are grouped under the "fields" key.

        Returns:
            A dictionary with:
              - "fields": individual component accuracies,
              - "acc": overall syntactic accuracy,
              - "errors": error messages for fields with issues.
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            return {"error": f"Invalid XML format: {e}"}
        
        field_scores = {}
        errors = {}

        # Check RegistrationPrefix (exactly 2 digits)
        reg_prefix_elem = root.find(self.xpaths.get("registration_prefix"))
        reg_prefix = reg_prefix_elem.text.strip() if reg_prefix_elem is not None and reg_prefix_elem.text else ""
        if re.fullmatch(r"\d{2}", reg_prefix):
            field_scores["registration_prefix_accuracy"] = 1.0
        else:
            field_scores["registration_prefix_accuracy"] = 0.0
            errors["registration_prefix"] = f"'{reg_prefix}' is not exactly 2 digits."

        # Check SeriesLetter (only English letters)
        series_letter_elem = root.find(self.xpaths.get("series_letter"))
        series_letter = series_letter_elem.text.strip() if series_letter_elem is not None and series_letter_elem.text else ""
        if re.fullmatch(r"[A-Za-z]+", series_letter):
            field_scores["series_letter_accuracy"] = 1.0
        else:
            field_scores["series_letter_accuracy"] = 0.0
            errors["series_letter"] = f"'{series_letter}' does not contain only English letters."

        # Check RegistrationNumber (exactly 3 digits)
        reg_number_elem = root.find(self.xpaths.get("registration_number"))
        reg_number = reg_number_elem.text.strip() if reg_number_elem is not None and reg_number_elem.text else ""
        if re.fullmatch(r"\d{3}", reg_number):
            field_scores["registration_number_accuracy"] = 1.0
        else:
            field_scores["registration_number_accuracy"] = 0.0
            errors["registration_number"] = f"'{reg_number}' is not exactly 3 digits."

        # Check ProvinceCode (1 or 2 digits)
        province_code_elem = root.find(self.xpaths.get("province_code"))
        province_code = province_code_elem.text.strip() if province_code_elem is not None and province_code_elem.text else ""
        if re.fullmatch(r"\d{1,2}", province_code):
            field_scores["province_code_accuracy"] = 1.0
        else:
            field_scores["province_code_accuracy"] = 0.0
            errors["province_code"] = f"'{province_code}' is not 1 or 2 digits."

        # Compute overall syntactic accuracy as the average of field scores.
        overall = sum(field_scores.values()) / len(field_scores) if field_scores else 0

        result = {
            "fields": field_scores,
            "file_accuracy": overall,
            "errors": errors
        }
        return result

    def process_folder(self) -> None:
        """
        Processes all XML files in the folder, computing the syntactic accuracy for each file,
        and storing the results in a dictionary mapping each filename to its results.
        """
        for filename in os.listdir(self.xml_folder):
            if filename.lower().endswith(".xml"):
                xml_path = os.path.join(self.xml_folder, filename)
                with open(xml_path, "r", encoding="utf-8") as f:
                    xml_content = f.read()
                self.results[filename] = self.compute_accuracy(xml_content)

    def get_syntactic_evaluator(self) -> str:
        """
        Generates a JSON report where for each file:
          - The accuracy for each field is grouped under "fields",
          - The overall syntactic accuracy is provided under "acc",
          - Any error messages are included under "errors".
        Additionally, a summary with the overall average accuracy is included.

        Returns:
            A JSON string of the report.
        """
        valid_files = [
            res for key, res in self.results.items()
            if key != "summary" and "file_accuracy" in res
        ]
        overall_accuracy = 0
        if valid_files:
            overall_accuracy = sum(res["file_accuracy"] for res in valid_files) / len(valid_files)
        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, indent=4)

# --- Example Usage ---
# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"
# xpaths = {
#     "registration_prefix": "LicensePlate/RegistrationPrefix",
#     "series_letter": "LicensePlate/SeriesLetter",
#     "registration_number": "LicensePlate/RegistrationNumber",
#     "province_code": "LicensePlate/ProvinceCode"
# }

# syntactic_evaluator = SyntacticAccuracy(xml_folder, xpaths)
# syntactic_evaluator.process_folder()
# report = syntactic_evaluator.get_syntactic_evaluator()
# print(report)


#output 

# {
#     "1000423.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000393.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000376.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000396.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000395.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000212.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 0.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 0.75,
#         "errors": {
#             "registration_prefix": "'' is not exactly 2 digits."
#         }
#     },
#     "1000229.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000244.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000211.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 1.0,
#             "series_letter_accuracy": 1.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 1.0,
#         "errors": {}
#     },
#     "1000198.xml": {
#         "fields": {
#             "registration_prefix_accuracy": 0.0,
#             "series_letter_accuracy": 0.0,
#             "registration_number_accuracy": 1.0,
#             "province_code_accuracy": 1.0
#         },
#         "file_accuracy": 0.5,
#         "errors": {
#             "registration_prefix": "'6522' is not exactly 2 digits.",
#             "series_letter": "'M11' does not contain only English letters."
#         }
#     },
#     "summary": {
#         "overall_accuracy": 0
#     }
# }