import os
import re
import json
import xml.etree.ElementTree as ET
from PIL import Image

class RiskOfInaccuracy:
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
        
        # Load Iranian Province Codes from JSON
        with open("data/IranProvinceCodes.json", "r", encoding="utf-8") as file:
            province_codes = json.load(file)
        self.valid_province_codes = {code for codes in province_codes.values() for code in codes}
        
        # English letters allowed in license plate series
        self.valid_series_letters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        
        # Updated Iranian Car Models
        self.valid_car_models = {
            "Mazda-2000", "Nissan-Zamiad", "Peugeot-206", "Peugeot-207i", "Peugeot-405", 
            "Peugeot-pars", "Peykan", "Pride-111", "Pride-131", "Quik", "Renault-L90", 
            "Samand", "Tiba2"
        }
        
        # Updated List of Valid Car Colors
        self.valid_road_colors = {
            "black", "white", "grey", "silver", "blue", "red", "green", "brown", 
            "beige", "golden", "bordeaux", "yellow", "violet", "orange"
        }
        
        # Set required fields (xpaths). Use defaults if not provided.
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
        Processes all XML files in the folder and checks for syntactic errors in the XML data.
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
        Validates the XML structure and its data against syntactic rules.
        
        Checks:
          - RegistrationPrefix: must be exactly 2 digits.
          - SeriesLetter: must contain only English letters.
          - RegistrationNumber: must be exactly 2 digits.
          - ProvinceCode: must be 1 or 2 digits (not exceeding 2 digits).
          - CarModel and CarColor are validated against predefined valid lists.
          - Coordinates (LicensePlate and Car) must be within the image dimensions.
        
        Returns a dictionary containing errors if any are found, or status "Valid".
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return {"error": "Invalid XML format"}

        issues = {}

        # Validate License Plate fields using the provided xpaths.
        reg_prefix = self.get_text(root, self.required_fields.get("registration_prefix"))
        series_letter = self.get_text(root, self.required_fields.get("series_letter"))
        reg_number = self.get_text(root, self.required_fields.get("registration_number"))
        province_code = self.get_text(root, self.required_fields.get("province_code"))

        # Convert RegistrationPrefix, RegistrationNumber, and ProvinceCode to integers if possible.
        try:
            reg_prefix_int = int(reg_prefix) if reg_prefix else None
            reg_number_int = int(reg_number) if reg_number else None
            province_code_int = int(province_code) if province_code else None
        except ValueError:
            issues["plate_fields"] = "Non-numeric value found in plate fields."
            reg_prefix_int = reg_number_int = province_code_int = None

        # Validate that plate prefix and number do not contain zeros.
        if reg_prefix_int is None or reg_prefix_int == 0 or '0' in str(reg_prefix_int):
            issues["registration_prefix"] = f"Invalid or missing registration prefix: '{reg_prefix}' (must be 2 digits, no zeros)."
        if reg_number_int is None or reg_number_int == 0 or '0' in str(reg_number_int):
            issues["registration_number"] = f"Invalid or missing registration number: '{reg_number}' (must be 2 digits, no zeros)."
        if series_letter is None or series_letter not in self.valid_series_letters:
            issues["series_letter"] = f"Invalid or missing series letter: '{series_letter}' (must contain only English letters)."
        if province_code_int is None or province_code_int not in self.valid_province_codes:
            issues["province_code"] = f"Invalid province code: '{province_code}'."
        
        # Validate Car Model and Car Color.
        car_model = self.get_text(root, self.required_fields.get("car_model"))
        if car_model not in self.valid_car_models:
            issues["car_model"] = f"Unexpected car model: '{car_model}'."
        
        car_color = self.get_text(root, self.required_fields.get("car_color"))
        if car_color is None or car_color.lower() not in self.valid_road_colors:
            issues["car_color"] = f"Unusual car color: '{car_color}'."
        
        # Validate Coordinates (if an image is available).
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size
                    license_coords = self.get_coordinates(root, self.required_fields.get("license_plate_coordinates"))
                    car_coords = self.get_coordinates(root, self.required_fields.get("car_coordinates"))
                    if not self.is_inside_image(license_coords, img_width, img_height):
                        issues["license_plate_coordinates"] = "License plate coordinates out of image bounds."
                    if not self.is_inside_image(car_coords, img_width, img_height):
                        issues["car_coordinates"] = "Car coordinates out of image bounds."
            except Exception as e:
                issues["image_error"] = str(e)
        
        return {"errors": issues} if issues else {"status": "Valid"}

    def get_text(self, root, path: str):
        """
        Extracts text from an XML element given its XPath.
        """
        element = root.find(path)
        return element.text.strip() if element is not None and element.text else None

    def get_coordinates(self, root, base_path: str) -> dict:
        """
        Extracts coordinate values from the XML and converts them to integers.
        Expects sub-elements X, Y, Width, Height under the given base_path.
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

    def get_risk_assessment(self) -> str:
        """
        Generates a JSON report summarizing the syntactic risk assessment
        (i.e. errors and overall validity) for all XML files in the folder.
        """
        total_files = len(self.results)
        valid_files = sum(1 for result in self.results.values() if "status" in result and result["status"] == "Valid")
        overall_accuracy = valid_files / total_files if total_files else 0

        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)

# --- Example Usage ---
# # Define folder paths.
# xml_folder = "/home/reza/Desktop/data-validation/img/Plate/xml"  # Folder containing XML files.
# image_folder = "/home/reza/Desktop/data-validation/img/Plate/img"  # Folder containing images.

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

# validator = RiskOfInaccuracy(xml_folder, image_folder, required_fields=custom_required_fields)
# validator.validate_files()
# print(validator.get_risk_assessment())


#out put

        # {
        #     "1000423.xml": {
        #         "errors": {
        #             "series_letter": "Invalid or missing series letter: 'Gh' (must contain only English letters)."
        #         }
        #     },
        #     "1000393.xml": {
        #         "status": "Valid"
        #     },
        #     "1000376.xml": {
        #         "status": "Valid"
        #     },
        #     "1000396.xml": {
        #         "errors": {
        #             "car_model": "Unexpected car model: 'Unknown'."
        #         }
        #     },
        #     "1000395.xml": {
        #         "status": "Valid"
        #     },
        #     "1000212.xml": {
        #         "errors": {
        #             "car_color": "Unusual car color: 'No car detected'."
        #         }
        #     },
        #     "1000229.xml": {
        #         "status": "Valid"
        #     },
        #     "1000244.xml": {
        #         "status": "Valid"
        #     },
        #     "1000211.xml": {
        #         "status": "Valid"
        #     },
        #     "1000198.xml": {
        #         "errors": {
        #             "series_letter": "Invalid or missing series letter: 'M11' (must contain only English letters)."
        #         }
        #     },
        #     "summary": {
        #         "overall_accuracy": 0.6
        #     }
        # }