import os
import json
import xml.etree.ElementTree as ET

def FeatureCompleteness(xml_folder: str, features: list) -> dict:
    """
    Checks for the presence of specified features (XPaths) in a folder containing XML files
    and calculates the presence rate for each feature (named as feature_completeness_file) as:
      (number of files where the feature is non-empty) / (total number of files)
    It also records the filenames where the feature is missing.
    
    Parameters:
      - xml_folder: the path to the folder containing XML files.
      - features: a list of XPath strings (e.g., "LicensePlate/RegistrationPrefix").
      
    Returns:
      A dictionary mapping each feature (XPath) to a dictionary containing:
          - "feature_completeness_file": the ratio of files in which the feature is present.
          - "missing_files": a list of filenames where the feature is missing or invalid.
      It also includes a "summary" entry with:
          - "mean_feature_completeness": the average feature_completeness_file across all features.
    """
    total_files = 0
    feature_stats = {feature: {"present": 0, "missing_files": []} for feature in features}
    
    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            total_files += 1
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError:
                # If the XML cannot be parsed, consider all features as missing in this file.
                for feature in features:
                    feature_stats[feature]["missing_files"].append(filename)
                continue
            
            for feature in features:
                elem = root.find(feature)
                # The feature is considered valid if the element exists and its text is non-empty.
                if elem is None or elem.text is None or elem.text.strip() == "":
                    feature_stats[feature]["missing_files"].append(filename)
                else:
                    feature_stats[feature]["present"] += 1
    
    results = {}
    total_feature_completeness = 0
    for feature in features:
        present = feature_stats[feature]["present"]
        # Compute the presence ratio (feature_completeness_file) for each feature.
        feature_completeness_file = present / total_files if total_files > 0 else 0
        results[feature] = {
            "feature_completeness_file": feature_completeness_file,
            "missing_files": feature_stats[feature]["missing_files"]
        }
        total_feature_completeness += feature_completeness_file
    
    # Compute the average presence ratio (feature_completeness_file) across all features.
    mean_feature_completeness = total_feature_completeness / len(features) if features else 0
    
    results["summary"] = {
        "feature_completeness": mean_feature_completeness
    }
    
    return json.dumps(results, ensure_ascii=False, indent=4)

# --- Example Usage ---

# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"

# features = [
#     "LicensePlate/RegistrationPrefix",
#     "LicensePlate/Serie2sLetter",
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

# completeness_report = FeatureCompleteness(xml_folder, features)
# print(completeness_report)


#output 

    # {
    #     "LicensePlate/RegistrationPrefix": {
    #         "feature_completeness_file": 0.9,
    #         "missing_files": [
    #             "1000212.xml"
    #         ]
    #     },
    #     "LicensePlate/Serie2sLetter": {
    #         "feature_completeness_file": 0.0,
    #         "missing_files": [
    #             "1000423.xml",
    #             "1000393.xml",
    #             "1000376.xml",
    #             "1000396.xml",
    #             "1000395.xml",
    #             "1000212.xml",
    #             "1000229.xml",
    #             "1000244.xml",
    #             "1000211.xml",
    #             "1000198.xml"
    #         ]
    #     },
    #     "LicensePlate/RegistrationNumber": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "LicensePlate/ProvinceCode": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "CarModel": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "CarColor": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "LicensePlateCoordinates/X": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "LicensePlateCoordinates/Y": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "LicensePlateCoordinates/Width": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "LicensePlateCoordinates/Height": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "CarCoordinates/X": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "CarCoordinates/Y": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "CarCoordinates/Width": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "CarCoordinates/Height": {
    #         "feature_completeness_file": 1.0,
    #         "missing_files": []
    #     },
    #     "summary": {
    #         "feature_completeness": 0.9214285714285715
    #     }
    # }