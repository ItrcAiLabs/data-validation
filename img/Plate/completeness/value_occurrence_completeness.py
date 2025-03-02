import os
import json
import xml.etree.ElementTree as ET

def ValueOccurrenceCompleteness(xml_folder: str, expected_counts: dict, field_xpaths: dict = None) -> dict:
    """
    Evaluates value occurrence completeness for features across a folder of XML files.
    
    For each feature:
      - Aggregates counts for each distinct value found in the XML files.
      - For each value, if its count >= the expected threshold (provided by the user), then
        its score is 1; otherwise, the score is (observed count) / (expected threshold).
      - The field completeness is the average of the scores for all values for that field.
    
    Parameters:
      xml_folder: path to the folder containing XML files.
      expected_counts: dictionary mapping field names to another dictionary mapping
                       distinct value (as string) to the expected threshold.
          For example:
              {
                  "CarColor": {"brown": 3, "purple": 2, "white": 5},
                  "CarModel": {"Peugeot-405": 10, "Samand": 8},
                  "RegistrationPrefix": {"48": 5, "63": 5}
              }
      field_xpaths: Optional dictionary mapping field names to their XPath in the XML.
          If not provided, the field name is assumed to be the XML tag.
    
    Returns:
      A dictionary with keys:
          - "features": mapping each field to:
              { "values": { value: {"count": count, "expected": expected, "score": score}, ... },
                "field_completeness": average_score_for_field }
          - "overall_completeness": average of field completeness scores.
    """
    # Initialize count dictionary for each field.
    field_counts = {field: {} for field in expected_counts.keys()}
    total_files = 0

    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            total_files += 1
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError:
                # If XML is invalid, skip this file.
                continue

            for field in expected_counts:
                # Use custom XPath if provided; otherwise assume tag equals field name.
                xpath = field_xpaths.get(field, field) if field_xpaths else field
                elem = root.find(xpath)
                # Consider the value as present if the element exists and its text is nonempty.
                value = elem.text.strip() if elem is not None and elem.text and elem.text.strip() != "" else "MISSING"
                field_counts[field][value] = field_counts[field].get(value, 0) + 1

    features_results = {}
    overall_field_scores = []

    for field, value_dict in field_counts.items():
        value_results = {}
        scores = []
        # expected_counts[field] should be a dictionary mapping value -> expected threshold.
        expected_for_field = expected_counts[field]
        for value, count in value_dict.items():
            # Get expected threshold for this value if provided.
            # If not provided, we can default to 1 (meaning any appearance gives a score of 1).
            expected_threshold = expected_for_field.get(value, 1)
            score = 1.0 if count >= expected_threshold else count / expected_threshold
            value_results[value] = {"count": count, "expected": expected_threshold, "score": score}
            scores.append(score)
        field_completeness = sum(scores) / len(scores) if scores else 0
        features_results[field] = {"values": value_results, "field_completeness": field_completeness}
        overall_field_scores.append(field_completeness)
    
    overall_completeness = sum(overall_field_scores) / len(overall_field_scores) if overall_field_scores else 0

    return {"features": features_results, "overall_completeness": overall_completeness, "total_files": total_files}

# --- Example Usage ---
# # Folder containing your XML files.
# xml_folder = "/home/reza/Desktop/data-validation/img/Plate/assets/xml"    # XML ground truth folder.

# # Expected counts: provide a dictionary for each field.
# expected_counts = {
#     "CarColor": {"brown": 3, "purple": 2, "white": 5},  # For example, expect at least 3 files with brown, 2 with purple, etc.
#     "CarModel": {"Peugeot-405": 10, "Samand": 8},
# }

# # Optionally, if the XML structure uses different tags than the field names,
# # provide a mapping from field to XPath. Otherwise, the field name is used directly.
# field_xpaths = {
#     "CarColor": "CarColor",
#     "CarModel": "CarModel",
#     "RegistrationPrefix": "LicensePlate/RegistrationPrefix"
# }

# results = value_occurrence_completeness(xml_folder, expected_counts, field_xpaths)
# print(json.dumps(results, ensure_ascii=False, indent=4))
#out put
# {
#     "features": {
#         "CarColor": {
#             "values": {
#                 "green": {
#                     "count": 2,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "grey": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "white": {
#                     "count": 3,
#                     "expected": 5,
#                     "score": 0.6
#                 },
#                 "silver": {
#                     "count": 2,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "No car detected": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "red": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 }
#             },
#             "field_completeness": 0.9333333333333332
#         },
#         "CarModel": {
#             "values": {
#                 "Peugeot-405": {
#                     "count": 4,
#                     "expected": 10,
#                     "score": 0.4
#                 },
#                 "Peugeot-207i": {
#                     "count": 2,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "Unknown": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "Peugeot-206": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "Pride-131": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 },
#                 "Peugeot-pars": {
#                     "count": 1,
#                     "expected": 1,
#                     "score": 1.0
#                 }
#             },
#             "field_completeness": 0.9
#         }
#     },
#     "overall_completeness": 0.9166666666666666,
#     "total_files": 10
# }