import xml.etree.ElementTree as ET
import json
import os
from PIL import Image

class RiskOfInaccuracy:
    def __init__(self, folder_path: str, image_folder: str) -> None:
        """
        Validates the structure and data correctness of Iranian car dataset.

        Parameters:
        - folder_path: Path to the folder containing XML files.
        - image_folder: Path to the folder containing images.
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

    def validate_files(self) -> None:
        """
        Processes all XML files and checks for errors in license plate, car color, car model, and coordinates.
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
        Validates the XML structure and its data.

        Returns:
        - Dictionary containing errors in license plate, car color, car model, and coordinates.
        """
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError:
            return {"error": "Invalid XML format"}

        issues = {}

        # Validate License Plate
        plate_prefix = self.get_text(root, "LicensePlate/RegistrationPrefix")
        series_letter = self.get_text(root, "LicensePlate/SeriesLetter")
        plate_number = self.get_text(root, "LicensePlate/RegistrationNumber")
        province_code = self.get_text(root, "LicensePlate/ProvinceCode")

        # Convert RegistrationPrefix and RegistrationNumber to integers, and check for zeros
        try:
            plate_prefix = int(plate_prefix) if plate_prefix else None
            plate_number = int(plate_number) if plate_number else None
            province_code = int(province_code) if province_code else None
        except ValueError:
            issues["plate_prefix"] = "Invalid plate prefix"
            issues["plate_number"] = "Invalid plate number"
            issues["province_code"] = "Invalid province code"
        
        # Validate plate prefix and plate number (ensure they do not contain zero)
        if plate_prefix == 0 or '0' in str(plate_prefix):  # Ensure there are no zeros
            issues["plate_prefix"] = "Invalid or missing plate prefix (cannot contain zeros)"
        if plate_number == 0 or '0' in str(plate_number):  # Ensure there are no zeros
            issues["plate_number"] = "Invalid or missing plate number (cannot contain zeros)"
        
        if not (series_letter and series_letter in self.valid_series_letters):
            issues["series_letter"] = "Invalid or missing series letter (must be English)"
        if province_code not in self.valid_province_codes:
            issues["province_code"] = f"Invalid province code: {province_code}"

        # Validate Car Model
        car_model = self.get_text(root, "CarModel")
        if car_model not in self.valid_car_models:
            issues["car_model"] = f"Unexpected car model: {car_model}"

        # Validate Car Color
        car_color = self.get_text(root, "CarColor")
        if car_color.lower() not in self.valid_road_colors:
            issues["car_color"] = f"Unusual car color: {car_color}"

        # Validate Coordinates inside Image
        if os.path.exists(image_path):
            try:
                with Image.open(image_path) as img:
                    img_width, img_height = img.size

                    license_coords = self.get_coordinates(root, "LicensePlateCoordinates")
                    car_coords = self.get_coordinates(root, "CarCoordinates")

                    if not self.is_inside_image(license_coords, img_width, img_height):
                        issues["license_plate_coordinates"] = "Coordinates out of image bounds"

                    if not self.is_inside_image(car_coords, img_width, img_height):
                        issues["car_coordinates"] = "Coordinates out of image bounds"
            except Exception as e:
                issues["image_error"] = str(e)

        return {"errors": issues} if issues else {"status": "Valid"}

    def get_text(self, root, path):
        """
        Extracts text from an XML tag.
        """
        element = root.find(path)
        return element.text.strip() if element is not None and element.text else None

    def get_coordinates(self, root, base_path):
        """
        Extracts coordinate values from XML and converts them to integers.
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

    def is_inside_image(self, coords, img_width, img_height):
        """
        Checks if coordinates are within image dimensions.
        """
        return (
            coords["x"] is not None and coords["y"] is not None and
            coords["width"] is not None and coords["height"] is not None and
            0 <= coords["x"] < img_width and 0 <= coords["y"] < img_height and
            coords["x"] + coords["width"] <= img_width and
            coords["y"] + coords["height"] <= img_height
        )

    def get_risk_assessment(self) -> str:
        """
        Generates a JSON report summarizing validation findings.

        Returns:
        - JSON string summarizing errors and overall dataset accuracy.
        """
        total_files = len(self.results)
        valid_files = sum(1 for result in self.results.values() if "status" in result and result["status"] == "Valid")
        overall_accuracy = valid_files / total_files if total_files else 0

        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)


# # Specify folder paths
# xml_folder = "/home/reza/Desktop/data-validation/img/Plate/xml"  
# image_folder = "/home/reza/Desktop/data-validation/img/Plate/img" 


# # Run validation
# validator = RiskOfInaccuracy(xml_folder, image_folder)
# validator.validate_files()
# print(validator.get_risk_assessment())
#out put 
    # {
    #     "1000423.xml": {
    #         "errors": {
    #             "series_letter": "Invalid or missing series letter (must be English)"
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
    #             "car_model": "Unexpected car model: Unknown"
    #         }
    #     },
    #     "1000395.xml": {
    #         "status": "Valid"
    #     },
    #     "1000212.xml": {
    #         "errors": {
    #             "car_color": "Unusual car color: No car detected"
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
    #         "status": "Valid"
    #     },
    #     "summary": {
    #         "overall_accuracy": 0.7
    #     }
    # }