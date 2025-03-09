import json
from .risk_of_inaccuracy import RiskOfInaccuracy
from .semantic_accuracy import SemanticEvaluator
from .data_model_accuracy import DataModelAccuracy
from .syntactic_accuracy import SyntacticAccuracy

def accuracy(image_folder, xml_folder, required_metadata, required_fields, allowed_file_types, dimension_range, file_size_range, xpaths_syntactic):
    """
    Runs the accuracy evaluation process and returns the report as a JSON-compatible dictionary.

    :param image_folder: Path to the folder containing images.
    :param xml_folder: Path to the folder containing XML files.
    :param required_metadata: Required metadata for data model evaluation.
    :param required_fields: Necessary fields for semantic accuracy evaluation.
    :param allowed_file_types: Allowed file formats for risk of inaccuracy evaluation.
    :param dimension_range: Valid image dimensions range.
    :param file_size_range: Valid file size range.
    :param xpaths_syntactic_evaluator: XPath fields for syntactic accuracy evaluation.

    :return: Dictionary containing the results of all evaluations.
    """

    results = {}
    # 1️⃣ Data Model Accuracy
    results["data_model_accuracy_xml"] = json.loads(DataModelAccuracy(image_folder, xml_folder, required_metadata, required_fields)[0])
    results["data_model_accuracy_img"] = json.loads(DataModelAccuracy(image_folder, xml_folder, required_metadata, required_fields)[1])

    # 2️⃣ Risk of Inaccuracy
    results["risk_of_inaccuracy_img"] = json.loads(RiskOfInaccuracy(image_folder, xml_folder, allowed_file_types, dimension_range, file_size_range, required_fields)[0])
    results["risk_of_inaccuracy_img"] = json.loads(RiskOfInaccuracy(image_folder, xml_folder, allowed_file_types, dimension_range, file_size_range, required_fields)[1])


    # 3️⃣ Semantic Accuracy
    semantic_evaluator = SemanticEvaluator(xml_folder, image_folder, required_fields)
    results["semantic_accuracy"] = json.loads(semantic_evaluator.evaluate_directory())


    # 4️⃣ Syntactic Accuracy
    syntactic_evaluator = SyntacticAccuracy(xml_folder, xpaths_syntactic)
    syntactic_evaluator.process_folder()
    results["syntactic_accuracy"] = json.loads(syntactic_evaluator.get_syntactic_evaluator())


    return json.dumps(results, ensure_ascii=False, indent=4)



# if __name__ == "__main__":
#     xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"
#     image_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/img"

#     required_metadata = ["width", "height", "format", "location", "date"]

#     required_fields = {
#         "registration_prefix": "LicensePlate/RegistrationPrefix",
#         "series_letter": "LicensePlate/SeriesLetter",
#         "registration_number": "LicensePlate/RegistrationNumber",
#         "province_code": "LicensePlate/ProvinceCode",
#         "car_model": "CarModel",
#         "car_color": "CarColor",
#         "license_plate_coordinates": "LicensePlateCoordinates",
#         "car_coordinates": "CarCoordinates"
#     }

#     allowed_file_types = ['png']

#     dimension_range = {
#         'min_width': 800,
#         'max_width': 1920,
#         'min_height': 600,
#         'max_height': 1080
#     }

#     file_size_range = {
#         'min_size': 1024,      
#         'max_size': 5_000_000  
#     }

#     xpaths_syntactic = {
#         "registration_prefix": "LicensePlate/RegistrationPrefix",
#         "series_letter": "LicensePlate/SeriesLetter",
#         "registration_number": "LicensePlate/RegistrationNumber",
#         "province_code": "LicensePlate/ProvinceCode"
#     }

#     report = accuracy(image_folder, xml_folder, required_metadata, required_fields, allowed_file_types, dimension_range, file_size_range, xpaths_syntactic)
    
#     print(report)
