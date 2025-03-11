import os
import json
import xml.etree.ElementTree as ET

def ValueOccurrenceCompleteness(xml_folder: str, expected_counts: dict, field_xpaths: dict = None) -> dict:
    """
    Evaluates value occurrence completeness for specified fields across a folder of XML files.
    
    For each field:
      - Aggregates counts for each distinct value found in the XML files.
      - For each value, if its count is greater than or equal to the expected threshold (provided by the user),
        the score is 1; otherwise, the score is (observed count) divided by (expected threshold).
      - The field completeness is the average of the scores for all values for that field.
    
    Parameters:
      xml_folder: The path to the folder containing XML files.
      expected_counts: A dictionary mapping field names to another dictionary mapping
                       distinct value (as a string) to the expected threshold.
          Example:
              {
                  "CarColor": {"brown": 3, "purple": 2, "white": 5},
                  "CarModel": {"Peugeot-405": 10, "Samand": 8},
                  "RegistrationPrefix": {"48": 5, "63": 5}
              }
      field_xpaths: Optional dictionary mapping field names to their XPath in the XML.
          If not provided, the field name is assumed to be the XML tag.
    
    Returns:
      A dictionary where each key is a field name mapped to a dictionary containing:
          - "values": a dictionary mapping each value to its count, expected threshold, and score.
          - "field_completeness": the average score for that field.
      Also includes a "summary" key with:
          - "overall_completeness": the average field completeness across all fields.
    """
    # Initialize a count dictionary for each field.
    field_counts = {field: {} for field in expected_counts.keys()}
    total_files = 0

    # Process each XML file in the folder.
    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            total_files += 1
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError:
                # If the XML is invalid, skip this file.
                continue

            # Iterate over each field defined in expected_counts.
            for field in expected_counts:
                # Use custom XPath if provided; otherwise, use the field name as the tag.
                xpath = field_xpaths.get(field, field) if field_xpaths else field
                elem = root.find(xpath)
                # Consider the value as present if the element exists and its text is nonempty.
                value = elem.text.strip() if elem is not None and elem.text and elem.text.strip() != "" else "MISSING"
                field_counts[field][value] = field_counts[field].get(value, 0) + 1

    features_results = {}
    overall_field_scores = []

    # Evaluate scores for each field.
    for field, value_dict in field_counts.items():
        value_results = {}
        scores = []
        # expected_counts[field] is a dictionary mapping value to the expected threshold.
        expected_for_field = expected_counts[field]
        for value, count in value_dict.items():
            # Use the provided expected threshold if available; default to 1 otherwise.
            expected_threshold = expected_for_field.get(value, 1)
            score = 1.0 if count >= expected_threshold else count / expected_threshold
            value_results[value] = {"count": count, "expected": expected_threshold, "score": score}
            scores.append(score)
        field_completeness = sum(scores) / len(scores) if scores else 0
        features_results[field] = {"values": value_results, "field_completeness": field_completeness}
        overall_field_scores.append(field_completeness)
    
    overall_completeness = sum(overall_field_scores) / len(overall_field_scores) if overall_field_scores else 0

    # Build final results with a structure similar to previous examples.
    results = {}
    for field in features_results:
        results[field] = features_results[field]
    
    results["summary"] = {
        "overall_completeness": overall_completeness
    }
    return json.dumps(results, ensure_ascii=False, indent=4)

# --- Example Usage ---
# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"

# expected_counts = {
#     "CarColor": {"brown": 3, "purple": 2, "white": 5},
#     "CarModel": {"Peugeot-405": 10, "Samand": 8},
# }

# field_xpaths = {
#     "CarColor": "CarColor",
#     "CarModel": "CarModel",
# }

# results = ValueOccurrenceCompleteness(xml_folder, expected_counts, field_xpaths)
# print(results)

# output 


# {
#     "CarColor": {
#         "values": {
#             "green": {
#                 "count": 2,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "grey": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "white": {
#                 "count": 3,
#                 "expected": 5,
#                 "score": 0.6
#             },
#             "silver": {
#                 "count": 2,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "No car detected": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "red": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             }
#         },
#         "field_completeness": 0.9333333333333332
#     },
#     "CarModel": {
#         "values": {
#             "Peugeot-405": {
#                 "count": 4,
#                 "expected": 10,
#                 "score": 0.4
#             },
#             "Peugeot-207i": {
#                 "count": 2,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "Unknown": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "Peugeot-206": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "Pride-131": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             },
#             "Peugeot-pars": {
#                 "count": 1,
#                 "expected": 1,
#                 "score": 1.0
#             }
#         },
#         "field_completeness": 0.9
#     },
#     "summary": {
#         "overall_completeness": 0.9166666666666666
#     }
# }