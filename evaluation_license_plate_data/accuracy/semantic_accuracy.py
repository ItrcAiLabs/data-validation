import os
import json
import xml.etree.ElementTree as ET
from PIL import Image
from ._semantic_accuracy.car_color_classifier.car_color_classifier_yolo4 import detect_car_color
from ._semantic_accuracy.iranian_car_detection.detection import detect_cars
from ._semantic_accuracy.Iranian_Plate_Recognitiont.plate_recognizer import process_image

class GetInfo:
    def __init__(self, image_path: str):
        self.image_path = image_path
    
    def extract_info(self):
        self.color = detect_car_color(self.image_path)
        self.car_model, car_bbox = detect_cars(self.image_path, save_output=False)
        self.car_coordinates = self.format_bbox(car_bbox)
        self.plate_number, plate_bbox = process_image(self.image_path)
        self.plate_coordinates = self.format_bbox(plate_bbox)
    
    def format_bbox(self, bbox):
        if bbox is None:
            return None
        x1, y1, x2, y2 = bbox
        return {"X": x1, "Y": y1, "Width": x2 - x1, "Height": y2 - y1}
    
    def parse_plate_number(self):
        plate = self.plate_number or ""
        if len(plate) < 8:
            return "##", "X", "###", "NN"
        reg_prefix = plate[:2]
        series_letter = next((c for c in plate[2:] if not c.isdigit()), "X")
        reg_number = plate[3:6] if len(plate) >= 6 else "###"
        province_code = plate[-2:] if len(plate) >= 2 else "NN"
        return reg_prefix, series_letter, reg_number, province_code


class XMLInfo:
    def __init__(self, xml_path: str, xml_config: dict):
        self.xml_path = xml_path
        self.xml_config = xml_config
        self.data = {}
        self.parse_xml()
    
    def parse_xml(self):
        try:
            tree = ET.parse(self.xml_path)
            root = tree.getroot()
            self.data = {key: self.get_text(root, path) for key, path in self.xml_config.items()}
        except ET.ParseError:
            self.data = {"error": "Invalid XML format"}
    
    def get_text(self, root, path):
        element = root.find(path)
        return element.text.strip() if element is not None and element.text else None


class SemanticEvaluator:
    def __init__(self, xml_dir: str, image_dir: str, xml_config: dict):
        self.xml_dir = xml_dir
        self.image_dir = image_dir
        self.xml_config = {key: xml_config[key] for key in xml_config if key in {
                                                                                    "registration_prefix",
                                                                                    "series_letter",
                                                                                    "registration_number",
                                                                                    "province_code",
                                                                                    "car_model",
                                                                                    "car_color",
                                                                                    "license_plate_coordinates_x",
                                                                                    "license_plate_coordinates_y",
                                                                                    "license_plate_coordinates_width",
                                                                                    "license_plate_coordinates_height",
                                                                                    "car_coordinates_x",
                                                                                    "car_coordinates_y",
                                                                                    "car_coordinates_width",
                                                                                    "car_coordinates_height"
                                                                                }}
        self.results = {}
    
    def evaluate_file(self, filename: str) -> dict:
        base_name = os.path.splitext(filename)[0]
        # Assume image files are in PNG format.
        img_path = os.path.join(self.image_dir, base_name + ".png")
        xml_path = os.path.join(self.xml_dir, base_name + ".xml")
        
        if not os.path.exists(xml_path):
            return {"error": f"Missing XML file for {filename}"}
        
        detector = GetInfo(img_path)
        detector.extract_info()
        reg_prefix, series_letter, reg_number, province_code = detector.parse_plate_number()
        # Update predictions with individual coordinate fields.
        pred_values = {
            "car_color": detector.color.lower() if detector.color else "",
            "car_model": detector.car_model,
            "registration_prefix": reg_prefix,
            "series_letter": series_letter,
            "registration_number": reg_number,
            "province_code": province_code,
            "license_plate_coordinates_x": detector.plate_coordinates.get("X") if detector.plate_coordinates else None,
            "license_plate_coordinates_y": detector.plate_coordinates.get("Y") if detector.plate_coordinates else None,
            "license_plate_coordinates_width": detector.plate_coordinates.get("Width") if detector.plate_coordinates else None,
            "license_plate_coordinates_height": detector.plate_coordinates.get("Height") if detector.plate_coordinates else None,
            "car_coordinates_x": detector.car_coordinates.get("X") if detector.car_coordinates else None,
            "car_coordinates_y": detector.car_coordinates.get("Y") if detector.car_coordinates else None,
            "car_coordinates_width": detector.car_coordinates.get("Width") if detector.car_coordinates else None,
            "car_coordinates_height": detector.car_coordinates.get("Height") if detector.car_coordinates else None
        }
        
        xml_info = XMLInfo(xml_path, self.xml_config)
        gt_data = xml_info.data
        
        field_scores = {}
        errors = []
        
        for field, pred_value in pred_values.items():
            gt_value = gt_data.get(field, None)
            # Compare string representations (or numerical values as strings) for coordinates.
            field_scores[f"{field}_accuracy"] = 1.0 if str(pred_value) == str(gt_value) else 0.0
            if str(pred_value) != str(gt_value):
                errors.append({
                    "field": field,
                    "predicted": pred_value,
                    "ground_truth": gt_value
                })
        
        overall_accuracy = sum(field_scores.values()) / len(field_scores) if field_scores else 0
        
        return {
            "fields": field_scores,
            "file_accuracy": overall_accuracy,
            "errors": errors
        }
    
    def evaluate_directory(self) -> dict:
        for filename in os.listdir(self.image_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                self.results[filename] = self.evaluate_file(filename)
        
        valid_files = [res for res in self.results.values() if "file_accuracy" in res]
        overall_accuracy = (sum(res["file_accuracy"] for res in valid_files) / len(valid_files)
                            if valid_files else 0)
        self.results["summary"] = {"overall_accuracy": overall_accuracy}
        return json.dumps(self.results, ensure_ascii=False, indent=4)


# xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"  # Folder containing XML files.
# image_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"   # Folder containing images.
    

# required_fields = {
#     "registration_prefix": "LicensePlate/RegistrationPrefix",
#     "series_letter": "LicensePlate/SeriesLetter",
#     "registration_number": "LicensePlate/RegistrationNumber",
#     "province_code": "LicensePlate/ProvinceCode",
#     "car_model": "CarModel",
#     "car_color": "CarColor",
#     "license_plate_coordinates": "LicensePlateCoordinates",
#     "car_coordinates": "CarCoordinates"
# }

# evaluator = SemanticEvaluator(xml_folder, image_folder, required_fields)
# results = evaluator.evaluate_directory()

# # Print the JSON report
# print(results)


#output


    # {
    #     "1000423.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 0.0,
    #             "registration_number_accuracy": 0.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.5,
    #         "errors": [
    #             {
    #                 "field": "series_letter",
    #                 "predicted": "G",
    #                 "ground_truth": "Gh"
    #             },
    #             {
    #                 "field": "registration_number",
    #                 "predicted": "h78",
    #                 "ground_truth": "787"
    #             },
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 52,
    #                     "Y": 2,
    #                     "Width": 1228,
    #                     "Height": 945
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 527,
    #                     "Y": 687,
    #                     "Width": 414,
    #                     "Height": 91
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000211.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 0,
    #                     "Y": 14,
    #                     "Width": 1217,
    #                     "Height": 1244
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 524,
    #                     "Y": 469,
    #                     "Width": 433,
    #                     "Height": 235
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000212.png": {
    #         "fields": {
    #             "car_color_accuracy": 0.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 0.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.5,
    #         "errors": [
    #             {
    #                 "field": "car_color",
    #                 "predicted": "no car detected",
    #                 "ground_truth": "No car detected"
    #             },
    #             {
    #                 "field": "registration_prefix",
    #                 "predicted": "88",
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 91,
    #                     "Y": 1,
    #                     "Width": 1189,
    #                     "Height": 1126
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 275,
    #                     "Y": 784,
    #                     "Width": 422,
    #                     "Height": 217
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000395.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 63,
    #                     "Y": 22,
    #                     "Width": 1189,
    #                     "Height": 887
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 473,
    #                     "Y": 699,
    #                     "Width": 418,
    #                     "Height": 116
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000396.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 0,
    #                     "Y": 0,
    #                     "Width": 0,
    #                     "Height": 0
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 351,
    #                     "Y": 471,
    #                     "Width": 469,
    #                     "Height": 127
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000244.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 14,
    #                     "Y": 0,
    #                     "Width": 1258,
    #                     "Height": 994
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 482,
    #                     "Y": 467,
    #                     "Width": 469,
    #                     "Height": 115
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000229.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 0,
    #                     "Y": 3,
    #                     "Width": 1278,
    #                     "Height": 571
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 635,
    #                     "Y": 785,
    #                     "Width": 409,
    #                     "Height": 124
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000393.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 174,
    #                     "Y": 129,
    #                     "Width": 955,
    #                     "Height": 760
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 483,
    #                     "Y": 527,
    #                     "Width": 345,
    #                     "Height": 81
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000198.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 0.0,
    #             "series_letter_accuracy": 0.0,
    #             "registration_number_accuracy": 0.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.375,
    #         "errors": [
    #             {
    #                 "field": "registration_prefix",
    #                 "predicted": "68",
    #                 "ground_truth": "6522"
    #             },
    #             {
    #                 "field": "series_letter",
    #                 "predicted": "M",
    #                 "ground_truth": "M11"
    #             },
    #             {
    #                 "field": "registration_number",
    #                 "predicted": "393",
    #                 "ground_truth": "3293"
    #             },
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 15,
    #                     "Y": 0,
    #                     "Width": 1260,
    #                     "Height": 1076
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 404,
    #                     "Y": 707,
    #                     "Width": 467,
    #                     "Height": 110
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "1000376.png": {
    #         "fields": {
    #             "car_color_accuracy": 1.0,
    #             "car_model_accuracy": 1.0,
    #             "registration_prefix_accuracy": 1.0,
    #             "series_letter_accuracy": 1.0,
    #             "registration_number_accuracy": 1.0,
    #             "province_code_accuracy": 1.0,
    #             "car_coordinates_accuracy": 0.0,
    #             "license_plate_coordinates_accuracy": 0.0
    #         },
    #         "acc": 0.75,
    #         "errors": [
    #             {
    #                 "field": "car_coordinates",
    #                 "predicted": {
    #                     "X": 31,
    #                     "Y": 10,
    #                     "Width": 1199,
    #                     "Height": 1020
    #                 },
    #                 "ground_truth": null
    #             },
    #             {
    #                 "field": "license_plate_coordinates",
    #                 "predicted": {
    #                     "X": 415,
    #                     "Y": 533,
    #                     "Width": 450,
    #                     "Height": 155
    #                 },
    #                 "ground_truth": null
    #             }
    #         ]
    #     },
    #     "summary": {
    #         "overall_accuracy": 0.6625
    #     }
    # }