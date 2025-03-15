import os
import json
import xml.etree.ElementTree as ET
from collections import defaultdict

def infer_type(value):
    """
    Infer the data type of a value: 'int', 'float', or 'str'.
    """
    try:
        int(value)
        return 'int'
    except ValueError:
        try:
            float(value)
            return 'float'
        except ValueError:
            return 'str'

def DataFormatConsistencyXml(xml_folder, xml_config):
    """
    Analyze data type consistency for fields across XML files in a folder.
    Includes an error section for files with inconsistent data types.

    Parameters:
    - xml_folder (str): Path to the folder containing XML files.
    - xml_config (dict): Dictionary mapping field names to XML paths.

    Returns:
    - dict: Report with field details (including errors for inconsistent files) and overall consistency score.
    """
    # List all XML files in the folder
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    
    # Initialize a dictionary to store data types and corresponding files for each field
    field_data = defaultdict(lambda: defaultdict(list))
    
    # Process each XML file
    for xml_file in xml_files:
        full_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(full_path)
        root = tree.getroot()
        
        # Extract values for each field and infer their types
        for field, path in xml_config.items():
            element = root.find(path)
            if element is not None and element.text is not None and element.text.strip() != "":
                data_type = infer_type(element.text.strip())
                field_data[field][data_type].append(xml_file)
    
    # Build the report
    report = {"fields": {}, "summary": {}}
    scores = []
    
    # Evaluate consistency for each field
    for field in xml_config.keys():
        types_dict = field_data[field]
        if types_dict:  # Field is present in at least one file
            # Find the most common type
            most_common_type = max(types_dict, key=lambda t: len(types_dict[t]))
            most_common_count = len(types_dict[most_common_type])
            total_files_with_field = sum(len(files) for files in types_dict.values())
            consistency_score = most_common_count / total_files_with_field
            # Error section: list files with types other than the most common type
            errors = [
                {"file": f, "actual_type": t}
                for t in types_dict if t != most_common_type
                for f in types_dict[t]
            ]
            report["fields"][field] = {
                "most_common_type": most_common_type,
                "consistency_score": consistency_score,
                "errors": errors
            }
        else:  # Field is missing in all files
            report["fields"][field] = {
                "most_common_type": None,
                "consistency_score": 0.0,
                "errors": [{"file": f, "actual_type": "missing"} for f in xml_files]
            }
        scores.append(report["fields"][field]["consistency_score"])
    
    # Calculate overall consistency as the average of field scores
    overall_consistency = sum(scores) / len(scores) if scores else 0.0
    report["summary"]["overall_consistency"] = overall_consistency
    
    return json.dumps(report, ensure_ascii=False, indent=4)

