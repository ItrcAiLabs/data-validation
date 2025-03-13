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
                                Expected keys (with new coordinate keys):
                                    - "registration_prefix": "LicensePlate/RegistrationPrefix"
                                    - "series_letter": "LicensePlate/SeriesLetter"
                                    - "registration_number": "LicensePlate/RegistrationNumber"
                                    - "province_code": "LicensePlate/ProvinceCode"
                                    - "car_model": "CarModel"
                                    - "car_color": "CarColor"
                                    - "license_plate_coordinates_x": "LicensePlateCoordinates/X"
                                    - "license_plate_coordinates_y": "LicensePlateCoordinates/Y"
                                    - "license_plate_coordinates_width": "LicensePlateCoordinates/Width"
                                    - "license_plate_coordinates_height": "LicensePlateCoordinates/Height"
                                    - "car_coordinates_x": "CarCoordinates/X"
                                    - "car_coordinates_y": "CarCoordinates/Y"
                                    - "car_coordinates_width": "CarCoordinates/Width"
                                    - "car_coordinates_height": "CarCoordinates/Height"
    
    Returns:
        tuple: A tuple containing two JSON reports:
            - report_xml: JSON report for XML file validation.
            - report_img: JSON report for image file validation.
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
    # The XML validator requires the image folder path to validate coordinate fields.
    xml_validator = RiskOfInaccuracyXml(xml_folder, img_folder, required_fields)
    # Process and validate all XML files in the specified folder.
    xml_validator.validate_files()
    # Get the JSON report for XML validation.
    report_xml = xml_validator.get_risk_inaccuracy()

    return report_xml, report_img


# ----------------------------
# Example usage:
# ----------------------------
# Specify the folder paths for XML files and images.
# xml_folder = "/home/reza/dev/data-validation/evaluation_license_plate_data/assets/xml"  # Folder containing XML files.
# img_folder = "//home/reza/dev/data-validation/evaluation_license_plate_data/assets/img"  # Folder containing image files.

# # Define custom required fields for XML validation using individual coordinate keys.
# custom_required_fields = {
#     "registration_prefix": "LicensePlate/RegistrationPrefix",
#     "series_letter": "LicensePlate/SeriesLetter",
#     "registration_number": "LicensePlate/RegistrationNumber",
#     "province_code": "LicensePlate/ProvinceCode",
#     "car_model": "CarModel",
#     "car_color": "CarColor",
#     "license_plate_coordinates_x": "LicensePlateCoordinates/X",
#     "license_plate_coordinates_y": "LicensePlateCoordinates/Y",
#     "license_plate_coordinates_width": "LicensePlateCoordinates/Width",
#     "license_plate_coordinates_height": "LicensePlateCoordinates/Height",
#     "car_coordinates_x": "CarCoordinates/X",
#     "car_coordinates_y": "CarCoordinates/Y",
#     "car_coordinates_width": "CarCoordinates/Width",
#     "car_coordinates_height": "CarCoordinates/Height"
# }

# # Define the allowed file types for image validation (e.g., only PNG images).
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
#     'min_size': 1024,       # Minimum 1 KB
#     'max_size': 5_000_000   # Maximum 5 MB
# }

# # Get the combined report for XML and image validations.
# report_xml, report_img = RiskOfInaccuracy(img_folder, xml_folder, allowed_file_types,
#                                             dimension_range, file_size_range, custom_required_fields)

# # Print the final JSON reports.
# print("XML Report:", report_xml)
# print("Image Report:", report_img)
