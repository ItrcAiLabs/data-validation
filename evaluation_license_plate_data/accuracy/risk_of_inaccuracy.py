from ._risk_of_inaccuracy.risk_of_inaccuracy_img import RiskOfInaccuracyImg
from ._risk_of_inaccuracy.risk_of_inaccuracy_xml import RiskOfInaccuracyXml


def RiskOfInaccuracy(img_folder, xml_folder, allowed_file_types, dimension_range, file_size_range, required_fields):
    """
    Validates both image files and XML files of a dataset using specified parameters.
    
    Parameters:
        img_folder (str): Path to the folder containing image files.
        xml_folder (str): Path to the folder containing XML files.
        allowed_file_types (list): List of allowed image file extensions (e.g., ['png']).
        dimension_range (dict): Dictionary with keys 'min_width', 'max_width', 'min_height', 'max_height'.
                                Example: {'min_width': 800, 'max_width': 1920, 'min_height': 600, 'max_height': 1080}.
        file_size_range (dict): Dictionary with keys 'min_size' and 'max_size' (in bytes).
                                Example: {'min_size': 1024, 'max_size': 5000000}.
        required_fields (dict): Dictionary mapping XML field names to their XPath locations.
                                Example:
                                {
                                    "registration_prefix": "LicensePlate/RegistrationPrefix",
                                    "series_letter": "LicensePlate/SeriesLetter",
                                    "registration_number": "LicensePlate/RegistrationNumber",
                                    "province_code": "LicensePlate/ProvinceCode",
                                    "car_model": "CarModel",
                                    "car_color": "CarColor",
                                    "license_plate_coordinates": "LicensePlateCoordinates",
                                    "car_coordinates": "CarCoordinates"
                                }
    
    Returns:
        list of reports.
    """
    
    # ----------------------------
    # Validate Images
    # ----------------------------
    # Create an instance of the image validator using the provided parameters.
    image_validator = RiskOfInaccuracyImg(img_folder, allowed_file_types, dimension_range, file_size_range)
    # Process and validate all image files in the folder.
    image_validator.validate_files()
    # Get the JSON report for image validation.
    report_img = image_validator.get_risk_inaccuracy()
    
    # ----------------------------
    # Validate XML Files
    # ----------------------------
    # Create an instance of the XML validator.
    # The XML validator also requires the image folder path (used for coordinate validation).
    xml_validator = RiskOfInaccuracyXml(xml_folder, img_folder, required_fields)
    # Process and validate all XML files in the specified folder.
    xml_validator.validate_files()
    # Get the JSON report for XML validation.
    report_xml = xml_validator.get_risk_inaccuracy()

    return report_xml, report_img
    

# Specify the folder paths for XML files and images.
# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"  # Folder containing XML files.
# image_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"   # Folder containing images.

# # Define custom required fields for XML validation.
# # If not provided, defaults defined in the RiskOfInaccuracyXml class are used.
# custom_required_fields = {
#     "registration_prefix": "LicensePlate/RegistrationPrefix",
#     "series_letter": "LicensePlate/SeriesLetter",
#     "registration_number": "LicensePlate/RegistrationNumber",
#     "province_code": "LicensePlate/ProvinceCode",
#     "car_model": "CarModel",
#     "car_color": "CarColor",
#     "license_plate_coordinates": "LicensePlateCoordinates",
#     "car_coordinates": "CarCoordinates"
# }

# # Define the allowed file types for image validation (only PNG images in this case).
# allowed_file_types = ['png']

# # Define the range for valid image dimensions.
# dimension_range = {
#     'min_width': 800,
#     'max_width': 1920,
#     'min_height': 600,
#     'max_height': 1080
# }

# # Define the allowed file size range (in bytes) for image validation.
# file_size_range = {
#     'min_size': 1024,      # Minimum 1 KB
#     'max_size': 5_000_000    # Maximum 5 MB
# }

# # Call the risk_of_inaccuracy function to get the combined report.
# report = RiskOfInaccuracy(image_folder, xml_folder, allowed_file_types, dimension_range, file_size_range, custom_required_fields)

# # Print the final combined JSON report.
# print(report)

#output

# ('{\n    "1000423.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000211.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000212.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000395.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000396.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000244.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000229.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000393.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000198.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "1000376.png": {\n        "fields": {\n            "file_type": 1,\n            "dimensions": 0,\n            "file_size": 1\n        },\n        "errors": {\n            "dimensions": "Image dimensions 1280x1280 are out of the allowed range: width [800, 1920], height [600, 1080]."\n        },\n        "file_accuracy": 0.6666666666666666\n    },\n    "summary": {\n        "overall_accuracy": 0.6666666666666666\n    }\n}', '{\n    "1000423.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 0,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "series_letter": "Invalid or missing series letter: \'Gh\' (must be exactly one English letter).",\n            "registration_number": "Invalid or missing registration number: \'787\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.5\n    },\n    "1000393.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'389\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.625\n    },\n    "1000376.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'687\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.625\n    },\n    "1000396.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 0,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'287\' (must be exactly 2 digits without zeros).",\n            "car_model": "Unexpected car model: \'Unknown\'.",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.5\n    },\n    "1000395.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'259\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.625\n    },\n    "1000212.xml": {\n        "fields": {\n            "registration_prefix": 0,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 0,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_prefix": "Invalid or missing registration prefix: \'None\' (must be exactly 2 digits without zeros).",\n            "registration_number": "Invalid or missing registration number: \'438\' (must be exactly 2 digits without zeros).",\n            "car_color": "Unusual car color: \'No car detected\'.",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.375\n    },\n    "1000229.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'617\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.625\n    },\n    "1000244.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'658\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.625\n    },\n    "1000211.xml": {\n        "fields": {\n            "registration_prefix": 1,\n            "series_letter": 1,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_number": "Invalid or missing registration number: \'615\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.625\n    },\n    "1000198.xml": {\n        "fields": {\n            "registration_prefix": 0,\n            "series_letter": 0,\n            "registration_number": 0,\n            "province_code": 1,\n            "car_model": 1,\n            "car_color": 1,\n            "license_plate_coordinates": 0,\n            "car_coordinates": 0\n        },\n        "errors": {\n            "registration_prefix": "Invalid or missing registration prefix: \'6522\' (must be exactly 2 digits without zeros).",\n            "series_letter": "Invalid or missing series letter: \'M11\' (must be exactly one English letter).",\n            "registration_number": "Invalid or missing registration number: \'393\' (must be exactly 2 digits without zeros).",\n            "license_plate_coordinates": "Image not found for license plate coordinates validation.",\n            "car_coordinates": "Image not found for car coordinates validation."\n        },\n        "file_accuracy": 0.375\n    },\n    "summary": {\n        "overall_accuracy": 0.55\n    }\n}')