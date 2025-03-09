import os
import re
import json
import xml.etree.ElementTree as ET
from PIL import Image

class RiskOfInaccuracyXml:
    def __init__(self, folder_path: str, image_folder: str, required_fields: dict = None) -> None:
        """
        Validates the structure and data correctness of an Iranian car dataset.
        
        Parameters:
            folder_path: Path to the folder containing XML files.
            image_folder: Path to the folder containing images.
            required_fields: Optional dictionary mapping field names to their XPath locations.
                Expected keys (with defaults):
                    - "registration_prefix": "LicensePlate/RegistrationPrefix"
                    - "series_letter": "LicensePlate/SeriesLetter"
                    - "registration_number": "LicensePlate/RegistrationNumber"
                    - "province_code": "LicensePlate/ProvinceCode"
                    - "car_model": "CarModel"
                    - "car_color": "CarColor"
                    - "license_plate_coordinates": "LicensePlateCoordinates"
                    - "car_coordinates": "CarCoordinates"
        """
        self.folder_path = folder_path
        self.image_folder = image_folder
        self.results = {}
        
        # Load valid province codes from JSON
        # with open("./_risk_of_inaccuracy/data/IranProvinceCodes.json", "r", encoding="utf-8") as file:
        #     province_codes = json.load(file)


        province_codes =  {
        "East Azerbaijan": [15, 25, 35],
        "West Azerbaijan": [17, 27, 37],
        "Ardabil": [91],
        "Isfahan": [13, 23, 43, 53, 67],
        "Alborz": [68, 78, 21, 38, 30],
        "Ilam": [98],
        "Bushehr": [48, 58],
        "Tehran": [11, 22, 33, 44, 55, 66, 77, 88, 99, 10, 20, 40],
        "Chaharmahal and Bakhtiari": [71, 81],
        "South Khorasan": [32, 52],
        "Razavi Khorasan": [12, 32, 42, 36, 74],
        "North Khorasan": [32, 26],
        "Khuzestan": [14, 24, 34],
        "Zanjan": [87, 97],
        "Semnan": [86, 96],
        "Sistan and Baluchestan": [85, 95],
        "Fars": [63, 73, 83, 93],
        "Qazvin": [79, 89],
        "Qom": [16],
        "Kurdistan": [51, 61],
        "Kerman": [45, 65, 75],
        "Kermanshah": [19, 29],
        "Kohgiluyeh and Boyer-Ahmad": [49],
        "Golestan": [59, 69],
        "Gilan": [46, 56, 76],
        "Lorestan": [31, 41],
        "Mazandaran": [62, 72, 82, 92],
        "Markazi": [47, 57],
        "Hormozgan": [84, 94],
        "Hamedan": [18, 28],
        "Yazd": [54, 64, 74]
    }

        # Convert to int for accurate comparison
        self.valid_province_codes = {int(code) for codes in province_codes.values() for code in codes}
        
        # Valid English letters for license plate series
        self.valid_series_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        # Updated list of valid car models
        self.valid_car_models = {
            "Mazda-2000", "Nissan-Zamiad", "Peugeot-206", "Peugeot-207i", "Peugeot-405", 
            "Peugeot-pars", "Peykan", "Pride-111", "Pride-131", "Quik", "Renault-L90", 
            "Samand", "Tiba2"
        }
        
        # Updated list of valid car colors
        self.valid_road_colors = {
            "black", "white", "grey", "silver", "blue", "red", "green", "brown", 
            "beige", "golden", "bordeaux", "yellow", "violet", "orange"
        }
        
        # Set required fields (xpaths). Defaults are used if not provided.
        default_required_fields = {
            "registration_prefix": "LicensePlate/RegistrationPrefix",
            "series_letter": "LicensePlate/SeriesLetter",
            "registration_number": "LicensePlate/RegistrationNumber",
            "province_code": "LicensePlate/ProvinceCode",
            "car_model": "CarModel",
            "car_color": "CarColor",
            "license_plate_coordinates": "LicensePlateCoordinates",
            "car_coordinates": "CarCoordinates"
        }
        self.required_fields = required_fields if required_fields is not None else default_required_fields

    def validate_files(self) -> None:
        """
        Process all XML files in the folder and validate their structure and data.
        For each file, it computes the score and error message for each field as well as the overall file accuracy.
        """
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".xml"):
                file_path = os.path.join(self.folder_path, filename)
                image_file = os.path.splitext(filename)[0] + ".jpg"
                image_path = os.path.join(self.image_folder, image_file)
                with open(file_path, "r", encoding="utf-8") as file:
                    xml_content = file.read()
                    self.results[filename] = self.validate_structure(xml_content, image_path)

    def validate_structure(self, xml_content: str, image_path: str) -> dict:
        """
        Validates the XML structure and data using the following rules:
          - registration_prefix: must be exactly 2 digits (without zeros).
          - series_letter: must be exactly one English letter.
          - registration_number: must be exactly 2 digits (without zeros).
          - province_code: must be 1 or 2 digits and be in the list of valid province codes.
          - car_model and car_color are validated against predefined lists.
          - Coordinates (for license plate and car) must be within the image bounds.
          
        For each field:
          - If valid, score is 1 and error message is empty.
          - If invalid, score is 0 and the corresponding error message is recorded.
          
        The overall file accuracy is computed as the average score of the fields.
        """
        field_scores = {}
        field_errors = {}
        total_fields = len(self.required_fields)
        
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            # If the XML is invalid, record an error for all fields.
            for field in self.required_fields:
                field_scores[field] = 0
                field_errors[field] = "Invalid XML format."
            return {"fields": field_scores, "errors": field_errors, "file_accuracy": 0}
        
        # Validate registration_prefix: must be exactly 2 digits (without zeros).
        reg_prefix = self.get_text(root, self.required_fields.get("registration_prefix"))
        if reg_prefix and re.fullmatch(r"[1-9]{2}", reg_prefix):
            field_scores["registration_prefix"] = 1
            field_errors["registration_prefix"] = ""
        else:
            field_scores["registration_prefix"] = 0
            field_errors["registration_prefix"] = f"Invalid or missing registration prefix: '{reg_prefix}' (must be exactly 2 digits without zeros)."
        
        # Validate series_letter: must be exactly one English letter.
        series_letter = self.get_text(root, self.required_fields.get("series_letter"))
        if series_letter and len(series_letter) == 1 and series_letter in self.valid_series_letters:
            field_scores["series_letter"] = 1
            field_errors["series_letter"] = ""
        else:
            field_scores["series_letter"] = 0
            field_errors["series_letter"] = f"Invalid or missing series letter: '{series_letter}' (must be exactly one English letter)."
        
        # Validate registration_number: must be exactly 2 digits (without zeros).
        reg_number = self.get_text(root, self.required_fields.get("registration_number"))
        if reg_number and re.fullmatch(r"[1-9]{2}", reg_number):
            field_scores["registration_number"] = 1
            field_errors["registration_number"] = ""
        else:
            field_scores["registration_number"] = 0
            field_errors["registration_number"] = f"Invalid or missing registration number: '{reg_number}' (must be exactly 2 digits without zeros)."
        
        # Validate province_code: must be 1 or 2 digits and be in the valid province codes.
        province_code = self.get_text(root, self.required_fields.get("province_code"))
        if province_code and re.fullmatch(r"[1-9]\d?", province_code):
            try:
                province_code_int = int(province_code)
                if province_code_int in self.valid_province_codes:
                    field_scores["province_code"] = 1
                    field_errors["province_code"] = ""
                else:
                    field_scores["province_code"] = 0
                    field_errors["province_code"] = f"Province code '{province_code}' is not in the valid list."
            except ValueError:
                field_scores["province_code"] = 0
                field_errors["province_code"] = f"Province code '{province_code}' cannot be converted to integer."
        else:
            field_scores["province_code"] = 0
            field_errors["province_code"] = f"Invalid province code: '{province_code}' (must be 1 or 2 digits and valid)."
        
        # Validate car_model
        car_model = self.get_text(root, self.required_fields.get("car_model"))
        if car_model in self.valid_car_models:
            field_scores["car_model"] = 1
            field_errors["car_model"] = ""
        else:
            field_scores["car_model"] = 0
            field_errors["car_model"] = f"Unexpected car model: '{car_model}'."
        
        # Validate car_color (case insensitive)
        car_color = self.get_text(root, self.required_fields.get("car_color"))
        if car_color and car_color.lower() in self.valid_road_colors:
            field_scores["car_color"] = 1
            field_errors["car_color"] = ""
        else:
            field_scores["car_color"] = 0
            field_errors["car_color"] = f"Unusual car color: '{car_color}'."
        
        # Validate coordinates: first check if the image exists.
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
                    # Validate license plate coordinates
                    license_coords = self.get_coordinates(root, self.required_fields.get("license_plate_coordinates"))
                    if self.is_inside_image(license_coords, img_width, img_height):
                        field_scores["license_plate_coordinates"] = 1
                        field_errors["license_plate_coordinates"] = ""
                    else:
                        field_scores["license_plate_coordinates"] = 0
                        field_errors["license_plate_coordinates"] = "License plate coordinates are out of image bounds or invalid."
                    
                    # Validate car coordinates
                    car_coords = self.get_coordinates(root, self.required_fields.get("car_coordinates"))
                    if self.is_inside_image(car_coords, img_width, img_height):
                        field_scores["car_coordinates"] = 1
                        field_errors["car_coordinates"] = ""
                    else:
                        field_scores["car_coordinates"] = 0
                        field_errors["car_coordinates"] = "Car coordinates are out of image bounds or invalid."
            except Exception as e:
                field_scores["license_plate_coordinates"] = 0
                field_errors["license_plate_coordinates"] = f"Error processing image: {e}"
                field_scores["car_coordinates"] = 0
                field_errors["car_coordinates"] = f"Error processing image: {e}"
        else:
            field_scores["license_plate_coordinates"] = 0
            field_errors["license_plate_coordinates"] = "Image not found for license plate coordinates validation."
            field_scores["car_coordinates"] = 0
            field_errors["car_coordinates"] = "Image not found for car coordinates validation."
        
        file_accuracy = sum(field_scores.values()) / total_fields
        
        # Remove empty error messages by creating a new dictionary
        field_errors = {key: value for key, value in field_errors.items() if value != ""}
        
        return {"fields": field_scores, "errors": field_errors, "file_accuracy": file_accuracy}

    def get_text(self, root, path: str):
        """
        Extract text from an XML element using XPath.
        """
        element = root.find(path)
        return element.text.strip() if element is not None and element.text else None

    def get_coordinates(self, root, base_path: str) -> dict:
        """
        Extract coordinates from XML and convert them to integers.
        Expects sub-elements X, Y, Width, Height under the given base path.
        """
        x = self.get_text(root, f"{base_path}/X")
        y = self.get_text(root, f"{base_path}/Y")
        width = self.get_text(root, f"{base_path}/Width")
        height = self.get_text(root, f"{base_path}/Height")
        return {
            "x": int(x) if x and x.isdigit() else None,
            "y": int(y) if y and y.isdigit() else None,
            "width": int(width) if width and width.isdigit() else None,
            "height": int(height) if height and height.isdigit() else None
        }

    def is_inside_image(self, coords: dict, img_width: int, img_height: int) -> bool:
        """
        Checks if the provided coordinates are within the image dimensions.
        """
        return (coords["x"] is not None and coords["y"] is not None and
                coords["width"] is not None and coords["height"] is not None and
                0 <= coords["x"] < img_width and 0 <= coords["y"] < img_height and
                coords["x"] + coords["width"] <= img_width and
                coords["y"] + coords["height"] <= img_height)

    def get_risk_inaccuracy(self) -> str:
        """
        Generates a JSON report where for each file:
          - The score for each field,
          - The error messages for each field,
          - The overall file accuracy (average score)
        And finally, the overall accuracy (average accuracy of all files) is included.
        """
        valid_file_results = [
            file_data 
            for key, file_data in self.results.items() 
            if key != "summary" and isinstance(file_data, dict)
        ]
        total_files = len(valid_file_results)
        overall_accuracy = 0
        if total_files > 0:
            overall_accuracy = sum(file_data["file_accuracy"] for file_data in valid_file_results) / total_files

        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)




# --- Example Usage ---
# # Define folder paths.
# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"  # Folder containing XML files.
# image_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"  # Folder containing images.

# # Optionally, the user can supply a custom required_fields dictionary.
# # If not provided, defaults (as specified in __init__) are used.
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

# validator = RiskOfInaccuracyXml(xml_folder, image_folder, required_fields=custom_required_fields)
# validator.validate_files()
# print(validator.get_risk_inaccuracy())

#out put

# {
#     "1000423.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 0,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "series_letter": "Invalid or missing series letter: 'Gh' (must be exactly one English letter).",
#             "registration_number": "Invalid or missing registration number: '787' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.5
#     },
#     "1000393.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '389' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.625
#     },
#     "1000376.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '687' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.625
#     },
#     "1000396.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 0,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '287' (must be exactly 2 digits without zeros).",
#             "car_model": "Unexpected car model: 'Unknown'.",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.5
#     },
#     "1000395.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '259' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.625
#     },
#     "1000212.xml": {
#         "fields": {
#             "registration_prefix": 0,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 0,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_prefix": "Invalid or missing registration prefix: 'None' (must be exactly 2 digits without zeros).",
#             "registration_number": "Invalid or missing registration number: '438' (must be exactly 2 digits without zeros).",
#             "car_color": "Unusual car color: 'No car detected'.",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.375
#     },
#     "1000229.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '617' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.625
#     },
#     "1000244.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '658' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.625
#     },
#     "1000211.xml": {
#         "fields": {
#             "registration_prefix": 1,
#             "series_letter": 1,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_number": "Invalid or missing registration number: '615' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.625
#     },
#     "1000198.xml": {
#         "fields": {
#             "registration_prefix": 0,
#             "series_letter": 0,
#             "registration_number": 0,
#             "province_code": 1,
#             "car_model": 1,
#             "car_color": 1,
#             "license_plate_coordinates": 0,
#             "car_coordinates": 0
#         },
#         "errors": {
#             "registration_prefix": "Invalid or missing registration prefix: '6522' (must be exactly 2 digits without zeros).",
#             "series_letter": "Invalid or missing series letter: 'M11' (must be exactly one English letter).",
#             "registration_number": "Invalid or missing registration number: '393' (must be exactly 2 digits without zeros).",
#             "license_plate_coordinates": "Image not found for license plate coordinates validation.",
#             "car_coordinates": "Image not found for car coordinates validation."
#         },
#         "file_accuracy": 0.375
#     },
#     "summary": {
#         "overall_accuracy": 0.55
#     }
# }