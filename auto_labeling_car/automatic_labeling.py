import os
import xml.etree.ElementTree as ET

from car_color_classifier.car_color_classifier_yolo4 import detect_car_color
from iranian_car_detection.detection import detect_cars
from Iranian_Plate_Recognitiont.plate_recognizer import detect_plate_chars, process_image

class Labeling:
    def __init__(self, source_dir: str, output_dir: str):
        self.source_dir = source_dir
        self.output_dir = output_dir
    def extract_info(self, img_path: str) -> None:
        """
        Runs detection on the given image and stores attributes as instance variables.
        """
        self.img_path = img_path

        # Detect car color.
        self.color = detect_car_color(self.img_path)

        # Detect car and get car coordinates along with its model.
        # Expected to return a tuple: (car_model, (x1, y1, x2, y2))
        self.car_model, (x1_car, y1_car, x2_car, y2_car) = detect_cars(self.img_path, save_output=False)
        self.car_coordinates = {
            "X": x1_car,
            "Y": y1_car,
            "Width": x2_car - x1_car,
            "Height": y2_car - y1_car
        }

        # Recognize license plate and get its coordinates.
        # Expected to return a tuple: (plate_number, (x1, y1, x2, y2))
        self.plate_number, (x1_plate, y1_plate, x2_plate, y2_plate) = process_image(self.img_path)
        self.plate_coordinates = {
            "X": x1_plate,
            "Y": y1_plate,
            "Width": x2_plate - x1_plate,
            "Height": y2_plate - y1_plate
        }

    def parse_plate_number(self):
        """
        Parses the recognized license plate into four parts:
        - RegistrationPrefix: first 2 characters.
        - SeriesLetter: all consecutive non-digit characters following the prefix (may be two or more characters).
        - RegistrationNumber: the next 3 characters (assumed to be digits).
        - ProvinceCode: the last 2 characters.
        If the plate format is unexpected, default placeholder values are returned.
        """
        plate = self.plate_number
        # Check if the plate exists and has a minimum expected length.
        if not plate or len(plate) < 8:
            return "##", "X", "###", "NN"
        
        # RegistrationPrefix: first 2 characters.
        reg_prefix = plate[:2]
        
        # SeriesLetter: accumulate consecutive non-digit characters starting from index 2.
        candidate_series = ""
        index = 2
        while index < len(plate) and not plate[index].isdigit():
            candidate_series += plate[index]
            index += 1
        if not candidate_series:
            candidate_series = "X"
        
        # RegistrationNumber: take the next 3 characters after the series letters.
        # If there are not enough characters, default to "###".
        if index + 3 <= len(plate):
            reg_number = plate[index:index+3]
        else:
            reg_number = "###"
        
        # ProvinceCode: the last 2 characters of the plate.
        province_code = plate[-2:] if len(plate) >= 2 else "NN"
        
        return reg_prefix, candidate_series, reg_number, province_code


    def save_xml(self, img_name: str) -> None:
        """
        Creates an XML file with the required structure containing:
          - License plate details (parsed from the recognized plate)
          - Car model (from detection)
          - Car color (from detection)
          - License plate coordinates and car coordinates
        The XML file is saved in the output directory using the image file's base name.
        """
        # Parse the plate number into components.
        reg_prefix, series_letter, reg_number, province_code = self.parse_plate_number()

        # Create XML structure.
        root = ET.Element("CarData")
        
        # LicensePlate block.
        license_plate = ET.SubElement(root, "LicensePlate")
        ET.SubElement(license_plate, "RegistrationPrefix").text = reg_prefix
        ET.SubElement(license_plate, "SeriesLetter").text = series_letter
        ET.SubElement(license_plate, "RegistrationNumber").text = reg_number
        ET.SubElement(license_plate, "ProvinceCode").text = province_code

        # CarModel element: save the detected car model.
        ET.SubElement(root, "CarModel").text = self.car_model if self.car_model else "Unknown"
        
        # CarColor from detection (or "Unknown" if not available).
        ET.SubElement(root, "CarColor").text = self.color if self.color else "Unknown"

        # LicensePlateCoordinates block.
        lp_coords = ET.SubElement(root, "LicensePlateCoordinates")
        ET.SubElement(lp_coords, "X").text = str(self.plate_coordinates.get("X", 0))
        ET.SubElement(lp_coords, "Y").text = str(self.plate_coordinates.get("Y", 0))
        ET.SubElement(lp_coords, "Width").text = str(self.plate_coordinates.get("Width", 0))
        ET.SubElement(lp_coords, "Height").text = str(self.plate_coordinates.get("Height", 0))

        # CarCoordinates block.
        car_coords = ET.SubElement(root, "CarCoordinates")
        ET.SubElement(car_coords, "X").text = str(self.car_coordinates.get("X", 0))
        ET.SubElement(car_coords, "Y").text = str(self.car_coordinates.get("Y", 0))
        ET.SubElement(car_coords, "Width").text = str(self.car_coordinates.get("Width", 0))
        ET.SubElement(car_coords, "Height").text = str(self.car_coordinates.get("Height", 0))

        # Ensure the output directory exists.
        os.makedirs(self.output_dir, exist_ok=True)

        # Use the image file's base name (with .xml extension) for the XML file.
        base_name = os.path.splitext(os.path.basename(img_name))[0]
        xml_file_path = os.path.join(self.output_dir, base_name + ".xml")

        # Write XML to file with declaration and UTF-8 encoding.
        tree = ET.ElementTree(root)
        tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)
        print(f"XML saved: {xml_file_path}")

    def process_directory(self) -> None:
        """
        Processes each image in the source directory.
        Supports common image extensions.
        """
        image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]
        for file in os.listdir(self.source_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                img_path = os.path.join(self.source_dir, file)
                print(f"Processing image: {img_path}")
                self.extract_info(img_path)
                self.save_xml(file)

if __name__ == "__main__":
    # Update these paths as needed.
    source_dir = "//home/reza/Downloads/alireza"  # Directory containing images to process.
    output_dir = "/home/reza/lable_xml"            # Output directory (ensure you have write permissions).
    
    labeling_instance = Labeling(source_dir, output_dir)
    labeling_instance.process_directory()
