from .feature_currentness import FeatureCurrentness
from .record_currentness import RecordCurrentness
import json

def Currentness(xml_folder: str, photo_folder: str, threshold_days: float, xml_config: dict) -> dict:
    """
    Combines feature and record currentness evaluations into a single report.

    It performs two evaluations:
      1. Feature Currentness Evaluation:
         - Uses FeatureCurrentness to assess how up-to-date the CarModel and CarColor
           values are in the XML files located in xml_folder.
         - Returns a dictionary with keys like "file_details" and "overall_feature_currentness".
      2. Record Currentness Evaluation:
         - Uses RecordCurrentness to assess the age of image files in photo_folder.
         - Returns a dictionary with keys such as "files" and "summary" (which includes overall_record_currentness).

    Parameters:
      xml_folder: Path to the folder containing XML files.
      photo_folder: Path to the folder containing image files.
      threshold_days: Age threshold (in days) to consider an image file as current.
      field_xpaths: Optional dictionary mapping feature names to their XPath in the XML.
                    Defaults to {"CarModel": "CarModel", "CarColor": "CarColor"}.

    Returns:
      A dictionary combining the results from both evaluations:
        {
          "feature_currentness": { ... FeatureCurrentness output ... },
          "record_currentness": { ... RecordCurrentness output ... }
        }
    """
    # Evaluate feature currentness from XML files.
    feature_report = FeatureCurrentness(xml_folder, xml_config)
    
    # Evaluate record currentness from photo files.
    record_report = RecordCurrentness(photo_folder, threshold_days)
    
    # Combine both reports into a single dictionary.
    combined_report = {
        "feature_currentness": json.loads(feature_report),
        "record_currentness": json.loads(record_report)
    }
    return json.dumps(combined_report, ensure_ascii=False, indent=4)
     
