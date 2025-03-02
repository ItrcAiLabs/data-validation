import os
import json
import xml.etree.ElementTree as ET

def feature_completeness(xml_folder: str, features: list) -> dict:
    """
    Checks a folder of XML files for the presence of a list of features (XPaths)
    and computes, for each feature, a precision defined as:
      (number of files where the feature is non-null) / (total number of files)
    Also records the file names in which each feature is missing.
    
    Parameters:
      - xml_folder: path to the folder containing XML files.
      - features: a list of XPath strings (e.g. "LicensePlate/RegistrationPrefix").
      
    Returns:
      A dictionary mapping each feature (XPath) to a dictionary with:
          - "precision": the fraction of files in which the feature is present.
          - "missing_files": a list of filenames where the feature is missing or empty.
      Also includes a "summary" entry with the total number of files processed.
    """
    total_files = 0
    feature_stats = {feature: {"present": 0, "missing_files": []} for feature in features}
    
    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            total_files += 1
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError as e:
                # If the XML cannot be parsed, mark all features as missing in this file.
                for feature in features:
                    feature_stats[feature]["missing_files"].append(filename)
                continue
            
            for feature in features:
                elem = root.find(feature)
                # Feature is considered present if element exists and its text is nonempty.
                if elem is None or elem.text is None or elem.text.strip() == "":
                    feature_stats[feature]["missing_files"].append(filename)
                else:
                    feature_stats[feature]["present"] += 1
    
    # Calculate precision for each feature.
    results = {}
    for feature in features:
        present = feature_stats[feature]["present"]
        precision = present / total_files if total_files > 0 else 0
        results[feature] = {
            "precision": precision,
            "missing_files": feature_stats[feature]["missing_files"]
        }
    
    results["summary"] = {"total_files": total_files}
    return results

# --- Example Usage ---
# # Define the folder containing your XML files.
# xml_folder = "/home/reza/Desktop/data-validation/img/Plate/assets/xml"    # XML ground truth folder.

# # Define the required features (XPaths) to check.
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

# # Compute the feature completeness.
# completeness_report = feature_completeness(xml_folder, features)
# print(json.dumps(completeness_report, ensure_ascii=False, indent=4))


# out put

# {
#     "LicensePlate/RegistrationPrefix": {
#         "precision": 0.9,
#         "missing_files": [
#             "1000212.xml"
#         ]
#     },
#     "LicensePlate/SeriesLetter": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "LicensePlate/RegistrationNumber": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "LicensePlate/ProvinceCode": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "CarModel": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "CarColor": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "LicensePlateCoordinates/X": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "LicensePlateCoordinates/Y": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "LicensePlateCoordinates/Width": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "LicensePlateCoordinates/Height": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "CarCoordinates/X": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "CarCoordinates/Y": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "CarCoordinates/Width": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "CarCoordinates/Height": {
#         "precision": 1.0,
#         "missing_files": []
#     },
#     "summary": {
#         "total_files": 10
#     }
# }