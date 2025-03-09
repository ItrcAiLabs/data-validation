from .feature_currentness import FeatureCurrentness
from .record_currentness import RecordCurrentness
import json

def Currentness(xml_folder: str, photo_folder: str, threshold_days: float, field_xpaths: dict = None) -> dict:
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
    feature_report = FeatureCurrentness(xml_folder, field_xpaths)
    
    # Evaluate record currentness from photo files.
    record_report = RecordCurrentness(photo_folder, threshold_days)
    
    # Combine both reports into a single dictionary.
    combined_report = {
        "feature_currentness": json.loads(feature_report),
        "record_currentness": json.loads(record_report)
    }
    return json.dumps(combined_report, ensure_ascii=False, indent=4)
     

# --- Example Usage ---
# if __name__ == "__main__":
#     xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"
#     photo_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"
#     threshold_days = 30  # A file is current if it is 30 days old or less.
#     field_xpaths = {"CarModel": "CarModel", "CarColor": "CarColor"}
    
#     report = Currentness(xml_folder, photo_folder, threshold_days, field_xpaths)
#     print(report)


#output


  # {
  #     "feature_currentness": {
  #         "file_details": {
  #             "1000423.xml": {
  #                 "CarModel": "Peugeot-405",
  #                 "CarModel_current": 1,
  #                 "CarColor": "green",
  #                 "CarColor_current": 0,
  #                 "Feature_currentness_file": 0.5
  #             },
  #             "1000393.xml": {
  #                 "CarModel": "Peugeot-405",
  #                 "CarModel_current": 1,
  #                 "CarColor": "grey",
  #                 "CarColor_current": 0,
  #                 "Feature_currentness_file": 0.5
  #             },
  #             "1000376.xml": {
  #                 "CarModel": "Peugeot-207i",
  #                 "CarModel_current": 0,
  #                 "CarColor": "white",
  #                 "CarColor_current": 1,
  #                 "Feature_currentness_file": 0.5
  #             },
  #             "1000396.xml": {
  #                 "CarModel": "Unknown",
  #                 "CarModel_current": 0,
  #                 "CarColor": "green",
  #                 "CarColor_current": 0,
  #                 "Feature_currentness_file": 0.0
  #             },
  #             "1000395.xml": {
  #                 "CarModel": "Peugeot-405",
  #                 "CarModel_current": 1,
  #                 "CarColor": "silver",
  #                 "CarColor_current": 1,
  #                 "Feature_currentness_file": 1.0
  #             },
  #             "1000212.xml": {
  #                 "CarModel": "Peugeot-206",
  #                 "CarModel_current": 0,
  #                 "CarColor": "No car detected",
  #                 "CarColor_current": 0,
  #                 "Feature_currentness_file": 0.0
  #             },
  #             "1000229.xml": {
  #                 "CarModel": "Pride-131",
  #                 "CarModel_current": 0,
  #                 "CarColor": "red",
  #                 "CarColor_current": 1,
  #                 "Feature_currentness_file": 0.5
  #             },
  #             "1000244.xml": {
  #                 "CarModel": "Peugeot-207i",
  #                 "CarModel_current": 0,
  #                 "CarColor": "white",
  #                 "CarColor_current": 1,
  #                 "Feature_currentness_file": 0.5
  #             },
  #             "1000211.xml": {
  #                 "CarModel": "Peugeot-pars",
  #                 "CarModel_current": 0,
  #                 "CarColor": "white",
  #                 "CarColor_current": 1,
  #                 "Feature_currentness_file": 0.5
  #             },
  #             "1000198.xml": {
  #                 "CarModel": "Peugeot-405",
  #                 "CarModel_current": 1,
  #                 "CarColor": "silver",
  #                 "CarColor_current": 1,
  #                 "Feature_currentness_file": 1.0
  #             }
  #         },
  #         "overall_feature_currentness": 0.5
  #     },
  #     "record_currentness": {
  #         "files": {
  #             "1000423.png": {
  #                 "age_days": 1383.8820423009577,
  #                 "record_currentness": 0
  #             },
  #             "1000211.png": {
  #                 "age_days": 1383.8826673009578,
  #                 "record_currentness": 0
  #             },
  #             "1000212.png": {
  #                 "age_days": 1383.8826441528097,
  #                 "record_currentness": 0
  #             },
  #             "1000395.png": {
  #                 "age_days": 1383.8821580416984,
  #                 "record_currentness": 0
  #             },
  #             "1000396.png": {
  #                 "age_days": 1383.8821580416984,
  #                 "record_currentness": 0
  #             },
  #             "1000244.png": {
  #                 "age_days": 1383.8825747083652,
  #                 "record_currentness": 0
  #             },
  #             "1000229.png": {
  #                 "age_days": 1383.8825978565133,
  #                 "record_currentness": 0
  #             },
  #             "1000393.png": {
  #                 "age_days": 1383.8821580416984,
  #                 "record_currentness": 0
  #             },
  #             "1000198.png": {
  #                 "age_days": 1383.8827830416985,
  #                 "record_currentness": 0
  #             },
  #             "1000376.png": {
  #                 "age_days": 1383.8822043379948,
  #                 "record_currentness": 0
  #             }
  #         },
  #         "summary": {
  #             "overall_record_currentness": 0.0
  #         }
  #     }
  # }