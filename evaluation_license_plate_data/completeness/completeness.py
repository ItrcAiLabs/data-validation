from .feature_completeness import FeatureCompleteness
from .record_completeness import RecordCompleteness
from .value_occurrence_completeness import ValueOccurrenceCompleteness
import json

def completeness(xml_folder: str, xml_config: dict, expected_counts: dict) -> dict:
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
    features = list(xml_config.values())
    feature_report = FeatureCompleteness(xml_folder, features)
    
    # 2. Record Completeness Evaluation
    record_report = RecordCompleteness(xml_folder, features)
    
    # 3. Value Occurrence Completeness Evaluation
    counts_x_path = {key: xml_config[key] for key in xml_config if key in {
                                                                                            "CarModel", 
                                                                                            "CarColor"    
                                                                                }}
    
    value_occurrence_report = ValueOccurrenceCompleteness(xml_folder, expected_counts, counts_x_path)
    
    # Combine all results into a single dictionary.
    all_results = {
        "feature_completeness": json.loads(feature_report),
        "record_completeness": json.loads(record_report),
        "value_occurrence_completeness": json.loads(value_occurrence_report)
    }
    

    
    return json.dumps(all_results, ensure_ascii=False, indent=4)
