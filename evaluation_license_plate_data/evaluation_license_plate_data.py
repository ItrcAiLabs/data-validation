from completeness.completeness import completeness
from accuracy.accuracy import accuracy
from currentness.currentness import Currentness
import json

def evaluation_license_plate_data(
    xml_folder: str,
    image_folder: str,
    threshold_days: float,
    features: list,
    expected_counts: dict,
    completeness_field_xpaths: dict,
    required_metadata: list,
    accuracy_required_fields: dict,
    allowed_file_types: list,
    dimension_range: dict,
    file_size_range: dict,
    xpaths_syntactic: dict,
    currentness_field_xpaths: dict = None
) -> str:
    """
    Runs the overall evaluation process for license plate data by combining:
      1. Completeness Evaluation:
         - Feature Completeness,
         - Record Completeness, and
         - Value Occurrence Completeness.
      2. Accuracy Evaluation:
         - Data Model Accuracy,
         - Risk of Inaccuracy,
         - Semantic Accuracy, and
         - Syntactic Accuracy.
      3. Currentness Evaluation:
         - Feature Currentness, and
         - Record Currentness.
    
    Note: The photo folder for currentness evaluation is the same as the image folder.
    
    Each sub-evaluation returns a JSON string; this function parses those strings,
    aggregates their results into a single dictionary, and then returns the combined
    report as a formatted JSON string.
    
    Parameters:
      xml_folder: Path to the folder containing XML files.
      image_folder: Path to the folder containing image files (used for both accuracy and currentness evaluation).
      threshold_days: Age threshold (in days) to consider an image file as current.
      
      -- For Completeness Evaluation --
      features: List of XPath strings for Feature Completeness evaluation.
      completeness_required_fields: List of required XPath strings for Record Completeness evaluation.
      expected_counts: Dictionary mapping field names to expected value counts for Value Occurrence Completeness.
      completeness_field_xpaths: Dictionary mapping field names to their XPath in the XML for Value Occurrence Completeness.
      
      -- For Accuracy Evaluation --
      required_metadata: List of required metadata fields for data model evaluation.
      accuracy_required_fields: Dictionary mapping field names to their XPath for semantic accuracy evaluation.
      allowed_file_types: List of allowed image file formats.
      dimension_range: Dictionary with valid image dimension ranges.
      file_size_range: Dictionary with valid file size range.
      xpaths_syntactic: Dictionary with XPath fields for syntactic accuracy evaluation.
      
      -- For Currentness Evaluation --
      currentness_field_xpaths: Optional dictionary mapping feature names to their XPath in the XML
                                for feature currentness evaluation. Defaults to {"CarModel": "CarModel", "CarColor": "CarColor"}.
    
    Returns:
      A JSON-formatted string that combines the results of:
          - Completeness Evaluation,
          - Accuracy Evaluation, and
          - Currentness Evaluation.
    """
    # Run Completeness Evaluation.
    comp_json_str = completeness(xml_folder, features, expected_counts, completeness_field_xpaths)
    comp_result = json.loads(comp_json_str)
    
    # Run Accuracy Evaluation.
    acc_json_str = accuracy(image_folder, xml_folder, required_metadata, accuracy_required_fields,
                            allowed_file_types, dimension_range, file_size_range, xpaths_syntactic)
    acc_result = json.loads(acc_json_str)
    
    # For Currentness Evaluation, use the same folder as image_folder.
    photo_folder = image_folder
    curr_json_str = Currentness(xml_folder, photo_folder, threshold_days, currentness_field_xpaths)
    curr_result = json.loads(curr_json_str)
    
    # Combine all results.
    overall_result = {
        "completeness": comp_result,
        "accuracy": acc_result,
        "currentness": curr_result
    }
    
    return json.dumps(overall_result, ensure_ascii=False, indent=4)

# --- Example Usage ---
if __name__ == "__main__":
    xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"
    image_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"
    threshold_days = 30  # A file is current if it is 30 days old or less.
    
    xml_config = {
        "registration_prefix": "LicensePlate/RegistrationPrefix",
        "series_letter": "LicensePlate/SeriesLetter",
        "registration_number": "LicensePlate/RegistrationNumber",
        "province_code": "LicensePlate/ProvinceCode",
        "car_model": "CarModel",
        "car_color": "CarColor",
        "license_plate_coordinates_x" : "LicensePlateCoordinates/X",
        "license_plate_coordinates_y" : "LicensePlateCoordinates/Y" ,
        "license_plate_coordinates_width" : "LicensePlateCoordinates/Width",
        "license_plate_coordinates_height" : "LicensePlateCoordinates/Height",
        "car_coordinates_x" : "CarCoordinates/X",
        "car_coordinates_y" : "CarCoordinates/Y",
        "car_coordinates_width" : "CarCoordinates/Width",
        "car_coordinates_height" : "CarCoordinates/Height"
        }
    # Parameters for Completeness Evaluation.
    features = list(xml_config.values())
    expected_counts = {
        "CarColor": {"brown": 3, "purple": 2, "white": 5},
        "CarModel": {"Peugeot-405": 10, "Samand": 8}
    }
    completeness_field_xpaths = {key: xml_config[key] for key in xml_config if key in {
                                                                                            "CarModel", 
                                                                                            "CarColor"    
                                                                                }}
    
    # Parameters for Accuracy Evaluation.
    required_metadata = ["width", "height", "format", "location", "date"]
    accuracy_required_fields= {key: xml_config[key] for key in xml_config if key in {
                                                                                        "registration_prefix", 
                                                                                        "series_letter", 
                                                                                        "registration_number", 
                                                                                        "province_code", 
                                                                                        "car_model", 
                                                                                        "car_color", 
                                                                                        "license_plate_coordinates", 
                                                                                        "car_coordinates"
                                                                                    }}
    allowed_file_types = ["png"]
    dimension_range = {
        "min_width": 800,
        "max_width": 1920,
        "min_height": 600,
        "max_height": 1080
    }
    file_size_range = {
        "min_size": 1024,
        "max_size": 5000000
    }
    
    xpaths_syntactic = {key: xml_config[key] for key in xml_config if key in {
                                                                                    "registration_prefix",
                                                                                    "series_letter",
                                                                                    "registration_number",
                                                                                    "province_code"
                                                                                }}
    

    
    # Parameter for Currentness Evaluation.
    currentness_field_xpaths = {key: xml_config[key] for key in xml_config if key in {
                                                                                            "CarModel", 
                                                                                            "CarColor"    
                                                                                }}
    
    # Run the overall evaluation.
    report = evaluation_license_plate_data(
        xml_folder,
        image_folder,
        threshold_days,
        features,
        expected_counts,
        completeness_field_xpaths,
        required_metadata,
        accuracy_required_fields,
        allowed_file_types,
        dimension_range,
        file_size_range,
        xpaths_syntactic,
        currentness_field_xpaths
    )
    
    print(report)
