import json
from .data_format_consistency import DataFormatConsistency
from .data_record_consistency import DataRecordConsistency
from .data_value_distribution import DataValueDistribution

def consistency(xml_folder, xml_config, img_path):
    """
    Computes multiple consistency checks and returns their results in a combined JSON format.
    
    This function calls:
      - DataValueDistribution: returns the distribution of unique values from XML files (as a JSON string).
      - DataFormatConsistency: returns the consistency of data formats comparing an image path and XML data (as a tuple).
      - DataRecordConsistency: returns the consistency of records in XML files (as a JSON string).
    
    Args:
        xml_folder (str): Path to the folder containing XML files.
        xml_config (dict): Dictionary mapping field names to XML paths.
        img_path (str): Path to the image file for format consistency checking.
    
    Returns:
        str: A JSON-formatted string containing the results of all three consistency checks.
    """
    # Get the data value distribution (expected to be a JSON string)
    value_distribution = json.loads(DataValueDistribution(xml_folder, xml_config))
    
    # DataFormatConsistency returns a tuple.
    # Assume the first element corresponds to image consistency and the second to XML consistency.
    format_consistency_img, format_consistency_xml = DataFormatConsistency(img_path, xml_folder, xml_config)
    
    # Get the record consistency (expected to be a JSON string)
    record_consistency = json.loads(DataRecordConsistency(xml_folder, img_path))
    
    # Combine all the results into a single dictionary
    combined_result = {
        "data_value_distribution": value_distribution,
        "data_format_consistency_img": json.loads(format_consistency_img),
        "data_format_consistency_xml": json.loads(format_consistency_xml),
        "data_record_consistency": record_consistency
    }
    
    # Return the combined result as a formatted JSON string
    return json.dumps(combined_result, ensure_ascii=False, indent=4)


