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
        A dictionary where each key is an XML filename (with its completeness score and missing fields)
        and a summary with overall completeness.
    """
    results = {}
    file_count = 0
    completeness_sum = 0.0

    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError as e:
                results[filename] = {"error": f"XML parse error: {e}"}
                continue

            total_fields = len(required_fields)
            present = 0
            missing_fields = []
            for field in required_fields:
                elem = root.find(field)
                if elem is None or elem.text is None or elem.text.strip() == "":
                    missing_fields.append(field)
                else:
                    present += 1

            file_completeness = present / total_fields if total_fields > 0 else 0
            completeness_sum += file_completeness
            file_count += 1

            results[filename] = {
                "completeness": file_completeness,
                "missing_fields": missing_fields
            }
    
    overall_completeness = completeness_sum / file_count if file_count > 0 else 0
    results["summary"] = {"overall_completeness": overall_completeness}
    return results

# --- Example Usage ---
# xml_folder = "/home/reza/Desktop/data-validation/img/Plate/assets/xml"    # XML ground truth folder.

# # Required fields as XPaths (customize these as needed).
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

# # Evaluate feature completeness.
# completeness_results = RecordCompleteness(xml_folder, required_fields)

# # Print the JSON report.
# print(json.dumps(completeness_results, ensure_ascii=False, indent=4))

#out put

    # {
    #     "1000423.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000393.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000376.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000396.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000395.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000212.xml": {
    #         "completeness": 0.9285714285714286,
    #         "missing_fields": [
    #             "LicensePlate/RegistrationPrefix"
    #         ]
    #     },
    #     "1000229.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000244.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000211.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "1000198.xml": {
    #         "completeness": 1.0,
    #         "missing_fields": []
    #     },
    #     "summary": {
    #         "overall_completeness": 0.9928571428571429
    #     }
    # }