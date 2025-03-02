import os
import sys
import json
import xml.etree.ElementTree as ET
from PIL import Image

# --- Adjust sys.path so that the project root and YOLOv5 folder are found ---

# If semantic_accuracy.py is at the project root, then its directory is the project root.


# --- External Detection Functions ---
from models.car_color_classifier.car_color_classifier_yolo4 import detect_car_color
from models.iranian_car_detection.detection import detect_cars
from models.Iranian_Plate_Recognitiont.plate_recognizer import detect_plate_chars, process_image

# --- Class to extract information from an image using the models ---
class GetInfo:
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
        - SeriesLetter: all consecutive non-digit characters following the prefix.
        - RegistrationNumber: the next 3 characters (assumed to be digits).
        - ProvinceCode: the last 2 characters.
        If the plate format is unexpected, default placeholder values are returned.
        """
        plate = self.plate_number
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
        if index + 3 <= len(plate):
            reg_number = plate[index:index+3]
        else:
            reg_number = "###"
        
        # ProvinceCode: the last 2 characters of the plate.
        province_code = plate[-2:] if len(plate) >= 2 else "NN"
        
        return reg_prefix, candidate_series, reg_number, province_code

# --- Class to extract ground truth info from an XML file ---
class XMLInfo:
    def __init__(self, xml_path: str):
        self.xml_path = xml_path
        self.parse_xml()

    def parse_xml(self) -> None:
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        # Extract ground truth using the expected XML paths.
        self.reg_prefix = self.get_text(root, "LicensePlate/RegistrationPrefix")
        self.series_letter = self.get_text(root, "LicensePlate/SeriesLetter")
        self.reg_number = self.get_text(root, "LicensePlate/RegistrationNumber")
        self.province_code = self.get_text(root, "LicensePlate/ProvinceCode")
        self.car_model = self.get_text(root, "CarModel")
        self.car_color = self.get_text(root, "CarColor")
        self.license_plate_coordinates = {
            "X": int(self.get_text(root, "LicensePlateCoordinates/X")),
            "Y": int(self.get_text(root, "LicensePlateCoordinates/Y")),
            "Width": int(self.get_text(root, "LicensePlateCoordinates/Width")),
            "Height": int(self.get_text(root, "LicensePlateCoordinates/Height"))
        }
        self.car_coordinates = {
            "X": int(self.get_text(root, "CarCoordinates/X")),
            "Y": int(self.get_text(root, "CarCoordinates/Y")),
            "Width": int(self.get_text(root, "CarCoordinates/Width")),
            "Height": int(self.get_text(root, "CarCoordinates/Height"))
        }

    def get_text(self, root, path: str) -> str:
        element = root.find(path)
        return element.text.strip() if element is not None and element.text else ""

# --- Evaluator Class: compares detected info from image with XML ground truth ---
class SemanticEvaluator:
    def __init__(self, xml_dir: str, image_dir: str, output_dir: str):
        """
        Initializes the evaluator with directories.
        - xml_dir: Directory containing XML ground truth files.
        - image_dir: Directory containing image files.
        - output_dir: (Optional) Directory for any output files.
        """
        self.xml_dir = xml_dir
        self.image_dir = image_dir
        self.output_dir = output_dir

    def evaluate_file(self, filename: str) -> dict:
        """
        Evaluates a single file by comparing information extracted from the image
        and its corresponding XML.
        """
        base_name = os.path.splitext(filename)[0]
        img_path = os.path.join(self.image_dir, base_name + ".jpg")
        xml_path = os.path.join(self.xml_dir, base_name + ".xml")

        # Get detected information from the image.
        detector = GetInfo(self.image_dir, self.output_dir)
        detector.extract_info(img_path)
        pred_color = detector.color.lower() if detector.color else ""
        pred_car_model = detector.car_model
        pred_car_coordinates = detector.car_coordinates
        pred_plate_coordinates = detector.plate_coordinates
        pred_reg_prefix, pred_series, pred_reg_number, pred_province = detector.parse_plate_number()

        # Get ground truth information from XML.
        xml_info = XMLInfo(xml_path)
        gt_color = xml_info.car_color.lower()
        gt_car_model = xml_info.car_model
        gt_car_coordinates = xml_info.car_coordinates
        gt_plate_coordinates = xml_info.license_plate_coordinates
        gt_reg_prefix = xml_info.reg_prefix
        gt_series = xml_info.series_letter
        gt_reg_number = xml_info.reg_number
        gt_province = xml_info.province_code

        scores = {}
        # Compare each semantic component.
        scores["color_accuracy"] = 1.0 if pred_color == gt_color else 0.0
        scores["registration_prefix_accuracy"] = 1.0 if pred_reg_prefix == gt_reg_prefix else 0.0
        scores["series_letter_accuracy"] = 1.0 if pred_series == gt_series else 0.0
        scores["registration_number_accuracy"] = 1.0 if pred_reg_number == gt_reg_number else 0.0
        scores["province_code_accuracy"] = 1.0 if pred_province == gt_province else 0.0
        scores["car_model_accuracy"] = 1.0 if pred_car_model == gt_car_model else 0.0
        scores["car_coordinates_accuracy"] = 1.0 if pred_car_coordinates == gt_car_coordinates else 0.0
        scores["plate_coordinates_accuracy"] = 1.0 if pred_plate_coordinates == gt_plate_coordinates else 0.0

        # Overall semantic accuracy: average of component scores.
        overall = sum(scores.values()) / len(scores)
        scores["overall_semantic_accuracy"] = overall

        # Include extracted values for reference.
        scores["predicted"] = {
            "color": pred_color,
            "registration_prefix": pred_reg_prefix,
            "series_letter": pred_series,
            "registration_number": pred_reg_number,
            "province_code": pred_province,
            "car_model": pred_car_model,
            "car_coordinates": pred_car_coordinates,
            "plate_coordinates": pred_plate_coordinates,
        }
        scores["ground_truth"] = {
            "color": gt_color,
            "registration_prefix": gt_reg_prefix,
            "series_letter": gt_series,
            "registration_number": gt_reg_number,
            "province_code": gt_province,
            "car_model": gt_car_model,
            "car_coordinates": gt_car_coordinates,
            "plate_coordinates": gt_plate_coordinates,
        }

        return scores

    def evaluate_directory(self) -> dict:
        """
        Evaluates all images in the image directory by comparing with corresponding XMLs.
        Returns a dictionary mapping each file to its semantic accuracy scores.
        """
        results = {}
        for filename in os.listdir(self.image_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                scores = self.evaluate_file(filename)
                results[filename] = scores
        # Compute overall average accuracy.
        if results:
            overall_accuracy = sum(item["overall_semantic_accuracy"] for key, item in results.items() if key != "summary") / len(results)
        else:
            overall_accuracy = 0
        results["summary"] = {"overall_accuracy": overall_accuracy}
        return results

# --- Example Usage ---
def main():
    # Define folder paths.
    xml_folder = "/home/reza/Desktop/data-validation/img/Plate/xml"    # XML ground truth folder.
    image_folder = "/home/reza/Desktop/data-validation/img/Plate/img"    # Image folder.
    output_dir = "/home/reza/Desktop/data-validation/output"             # Optional output folder.
    
    evaluator = SemanticEvaluator(xml_folder, image_folder, output_dir)
    results = evaluator.evaluate_directory()
    
    # Print the JSON report.
    report = json.dumps(results, ensure_ascii=False, indent=4)
    print(report)

if __name__ == "__main__":
    main()
