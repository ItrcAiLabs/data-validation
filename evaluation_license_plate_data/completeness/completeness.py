from .feature_completeness import FeatureCompleteness
from .record_completeness import RecordCompleteness
from .value_occurrence_completeness import ValueOccurrenceCompleteness
import json

def completeness(xml_folder: str, features: list, expected_counts: dict, field_xpaths: dict) -> dict:
    """
    Runs three completeness evaluations on the XML files in the specified folder:
      1. Feature Completeness Evaluation:
         Checks for the presence of required features (XPaths) in each XML file.
      2. Record Completeness Evaluation:
         Computes the completeness score for each XML file based on required fields.
      3. Value Occurrence Completeness Evaluation:
         Evaluates the occurrence of specific values compared to expected thresholds.
    
    The results from all evaluations are combined into a single dictionary and written
    to a JSON file ("completeness_report.json").
    
    Parameters:
        xml_folder: The folder containing XML files.
        features: List of XPath strings for Feature Completeness evaluation.
        required_fields: List of required XPath strings for Record Completeness evaluation.
        expected_counts: Dictionary mapping field names to dictionaries of expected value counts.
        field_xpaths: Dictionary mapping field names to their XPath in the XML for Value Occurrence Completeness.
        
    Returns:
        A dictionary containing:
            - "feature_completeness": Result from FeatureCompleteness.
            - "record_completeness": Result from RecordCompleteness.
            - "value_occurrence_completeness": Result from ValueOccurrenceCompleteness.
    """
    # 1. Feature Completeness Evaluation
    feature_report = FeatureCompleteness(xml_folder, features)
    
    # 2. Record Completeness Evaluation
    record_report = RecordCompleteness(xml_folder, features)
    
    # 3. Value Occurrence Completeness Evaluation
    value_occurrence_report = ValueOccurrenceCompleteness(xml_folder, expected_counts, field_xpaths)
    
    # Combine all results into a single dictionary.
    all_results = {
        "feature_completeness": json.loads(feature_report),
        "record_completeness": json.loads(record_report),
        "value_occurrence_completeness": json.loads(value_occurrence_report)
    }
    

    
    return json.dumps(all_results, ensure_ascii=False, indent=4)

# --- Example Usage ---
# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"

# features = [
#     "LicensePlate/RegistrationPrefix",
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

# required_fields = [
#     "LicensePlate/RegistrationPrefix",
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

# expected_counts = {
#     "CarColor": {"brown": 3, "purple": 2, "white": 5},
#     "CarModel": {"Peugeot-405": 10, "Samand": 8},
# }

# field_xpaths = {
#     "CarColor": "CarColor",
#     "CarModel": "CarModel",
#     "RegistrationPrefix": "LicensePlate/RegistrationPrefix"
# }

# results = completeness(xml_folder, features, expected_counts, field_xpaths)
# print(results)
