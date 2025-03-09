import os
import json
import xml.etree.ElementTree as ET

def RecordCompleteness(xml_folder: str, required_fields: list) -> dict:
    """
    Processes all XML files in the given folder and computes the Record Completeness for each file.
    
    Parameters:
        xml_folder: The directory path containing XML files.
        required_fields: A list of XPath strings indicating the required fields in each XML file.
        
    Returns:
        A dictionary where each key is an XML filename mapped to a dictionary containing:
            - "record_completeness_file": the completeness score for that file.
            - "missing_fields": a list of required fields that are missing or empty in that file.
        Additionally, it includes a "summary" key with:
            - "mean_record_completeness": the average record completeness score across all files.
    """
    results = {}
    file_count = 0
    completeness_sum = 0.0

    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            file_count += 1
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError as e:
                # If the XML cannot be parsed, record an error for this file.
                results[filename] = {"error": f"XML parse error: {e}"}
                continue

            total_fields = len(required_fields)
            present = 0
            missing_fields = []
            for field in required_fields:
                elem = root.find(field)
                # A field is considered present if the element exists and its text is non-empty.
                if elem is None or elem.text is None or elem.text.strip() == "":
                    missing_fields.append(field)
                else:
                    present += 1

            # Calculate the record completeness for the file.
            record_completeness_file = present / total_fields if total_fields > 0 else 0
            completeness_sum += record_completeness_file

            results[filename] = {
                "record_completeness_file": record_completeness_file,
                "missing_fields": missing_fields
            }
    
    # Compute the average record completeness across all files.
    mean_record_completeness = completeness_sum / file_count if file_count > 0 else 0
    results["summary"] = {
        "record_completeness": mean_record_completeness
    }
    return json.dumps(results, ensure_ascii=False, indent=4)

# --- Example Usage ---
# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"

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

# completeness_results = RecordCompleteness(xml_folder, required_fields)
# print(completeness_results)


#output

    # {
    #     "1000423.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000393.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000376.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000396.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000395.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000212.xml": {
    #         "record_completeness_file": 0.9285714285714286,
    #         "missing_fields": [
    #             "LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000229.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000244.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000211.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000198.xml": {
    #         "record_completeness_file": 1.0,
    #         "missing_fields": []
    #     },
    #     "summary": {
    #         "record_completeness": 0.9928571428571429
    #     }
    # }