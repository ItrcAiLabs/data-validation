import os
import re
import json
import xml.etree.ElementTree as ET

def syntactic_accuracy(xml_content: str, xpaths: dict) -> dict:
    """
    Computes the syntactic accuracy for Iranian vehicle license plate components
    based on an XML string and a dictionary specifying the XML paths for each field.
    
    Expected keys in xpaths:
      - "registration_prefix": e.g. "LicensePlate/RegistrationPrefix"
      - "series_letter": e.g. "LicensePlate/SeriesLetter"
      - "registration_number": e.g. "LicensePlate/RegistrationNumber"
      - "province_code": e.g. "LicensePlate/ProvinceCode"
      
    Checks:
      - RegistrationPrefix must match exactly two digits.
      - SeriesLetter must consist solely of English letters (A-Z or a-z).
      - RegistrationNumber must match exactly two digits.
      - ProvinceCode must match one or two digits (i.e. not exceed 2 digits).
    
    Returns a dictionary with individual component accuracies (1.0 for correct, 0.0 for error),
    an overall syntactic accuracy (average of all components), and an "errors" dictionary.
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        return {"error": f"Invalid XML format: {e}"}
    
    results = {}
    errors = {}

    # Check RegistrationPrefix (exactly 2 digits)
    reg_prefix_elem = root.find(xpaths.get("registration_prefix"))
    reg_prefix = reg_prefix_elem.text.strip() if reg_prefix_elem is not None and reg_prefix_elem.text else ""
    if re.fullmatch(r"\d{2}", reg_prefix):
        results["registration_prefix_accuracy"] = 1.0
    else:
        results["registration_prefix_accuracy"] = 0.0
        errors["registration_prefix"] = f"'{reg_prefix}' is not exactly 2 digits."
    
    # Check SeriesLetter (only English letters)
    series_letter_elem = root.find(xpaths.get("series_letter"))
    series_letter = series_letter_elem.text.strip() if series_letter_elem is not None and series_letter_elem.text else ""
    if re.fullmatch(r"[A-Za-z]+", series_letter):
        results["series_letter_accuracy"] = 1.0
    else:
        results["series_letter_accuracy"] = 0.0
        errors["series_letter"] = f"'{series_letter}' does not contain only English letters."
    
    # Check RegistrationNumber (exactly 2 digits)
    reg_number_elem = root.find(xpaths.get("registration_number"))
    reg_number = reg_number_elem.text.strip() if reg_number_elem is not None and reg_number_elem.text else ""
    if re.fullmatch(r"\d{2}", reg_number):
        results["registration_number_accuracy"] = 1.0
    else:
        results["registration_number_accuracy"] = 0.0
        errors["registration_number"] = f"'{reg_number}' is not exactly 2 digits."
    
    # Check ProvinceCode (1 or 2 digits)
    province_code_elem = root.find(xpaths.get("province_code"))
    province_code = province_code_elem.text.strip() if province_code_elem is not None and province_code_elem.text else ""
    if re.fullmatch(r"\d{1,2}", province_code):
        results["province_code_accuracy"] = 1.0
    else:
        results["province_code_accuracy"] = 0.0
        errors["province_code"] = f"'{province_code}' is not 1 or 2 digits."

    # Compute overall syntactic accuracy as the average of component scores.
    overall = sum(results.values()) / len(results) if results else 0
    results["overall_syntactic_accuracy"] = overall
    results["errors"] = errors

    return results

def evaluate_folder(xml_folder: str, xpaths: dict) -> dict:
    """
    Processes all XML files in a folder, computing the syntactic accuracy for each,
    and then computes an overall average accuracy.
    
    Returns a dictionary mapping each XML filename to its syntactic accuracy results,
    and a summary with overall accuracy.
    """
    results = {}
    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            xml_path = os.path.join(xml_folder, filename)
            with open(xml_path, "r", encoding="utf-8") as f:
                xml_content = f.read()
            file_result = syntactic_accuracy(xml_content, xpaths)
            results[filename] = file_result
    # Compute overall average accuracy across files.
    valid_files = [res for res in results.values() if "overall_syntactic_accuracy" in res]
    if valid_files:
        overall_accuracy = sum(res["overall_syntactic_accuracy"] for res in valid_files) / len(valid_files)
    else:
        overall_accuracy = 0
    results["summary"] = {"overall_accuracy": overall_accuracy}
    return results

# --- Example Usage ---
if __name__ == "__main__":
    # Define the folder containing the XML files.
    xml_folder = "/home/reza/Desktop/data-validation/img/Plate/xml"    # XML ground truth folder.
    
    # Define the XML paths for each field.
    xpaths = {
        "registration_prefix": "LicensePlate/RegistrationPrefix",
        "series_letter": "LicensePlate/SeriesLetter",
        "registration_number": "LicensePlate/RegistrationNumber",
        "province_code": "LicensePlate/ProvinceCode"
    }
    
    # Evaluate the folder.
    accuracy_results = evaluate_folder(xml_folder, xpaths)
    
    # Print the JSON report.
    print(json.dumps(accuracy_results, indent=4))
# output
    # {
    #     "1000423.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'787' is not exactly 2 digits."
    #         }
    #     },
    #     "1000393.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'389' is not exactly 2 digits."
    #         }
    #     },
    #     "1000376.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'687' is not exactly 2 digits."
    #         }
    #     },
    #     "1000396.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'287' is not exactly 2 digits."
    #         }
    #     },
    #     "1000395.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'259' is not exactly 2 digits."
    #         }
    #     },
    #     "1000212.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'438' is not exactly 2 digits."
    #         }
    #     },
    #     "1000229.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'617' is not exactly 2 digits."
    #         }
    #     },
    #     "1000244.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'658' is not exactly 2 digits."
    #         }
    #     },
    #     "1000211.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'615' is not exactly 2 digits."
    #         }
    #     },
    #     "1000198.xml": {
    #         "registration_prefix_accuracy": 1.0,
    #         "series_letter_accuracy": 1.0,
    #         "registration_number_accuracy": 0.0,
    #         "province_code_accuracy": 1.0,
    #         "overall_syntactic_accuracy": 0.75,
    #         "errors": {
    #             "registration_number": "'393' is not exactly 2 digits."
    #         }
    #     },
    #     "summary": {
    #         "overall_accuracy": 0.75
    #     }
    # }
