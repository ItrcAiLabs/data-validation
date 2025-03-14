import os
import json
import xml.etree.ElementTree as ET

def FeatureCurrentness(xml_folder: str, xml_config: dict = None) -> dict:
    """
    Evaluates how up-to-date each feature is across all XML files.

    The function loads up-to-date values from two JSON files:
      - "data/new_colors.json": should contain {"colors": [ ... ]}
      - "data/new_cars.json": should contain {"cars": [ ... ]}

    For each XML file in xml_folder, the function extracts the CarModel and CarColor
    using provided XPaths (defaults to "CarModel" and "CarColor") and checks whether each
    value is in the corresponding up-to-date list loaded from the JSON files.

    It aggregates counts for each feature:
      - Total number of files processed for that feature.
      - Number of files where the feature is up-to-date.
      - Precision: (up-to-date count) / (total files).

    Additionally, it collects file-level details including the extracted values and an overall
    score (average of CarModel and CarColor scores) for each file.

    Parameters:
      xml_folder: Path to the folder containing XML files.
      field_xpaths: Optional dictionary mapping feature names to their XPath in the XML.
                    Defaults to {"CarModel": "CarModel", "CarColor": "CarColor"}.

    Returns:
      A dictionary with:
        - "file_details": a mapping of each XML file to its extracted values and overall file score.
        - "overall_feature_currentness": average of the feature precisions.
    """

    field_xpaths = {key: xml_config[key] for key in xml_config if key in {
                                                                                            "CarModel", 
                                                                                            "CarColor"    
                                                                                }}
    # Load up-to-date values from JSON files.
    with open("./currentness/data/CarColor.json", "r", encoding="utf-8") as f:
        colors_data = json.load(f)
    with open("./currentness/data/CarModel.json", "r", encoding="utf-8") as f:
        cars_data = json.load(f)
    
    # Build up-to-date values summary.
    up_to_date_values = {
        "CarColor": colors_data.get("colors", []),
        "CarModel": cars_data.get("cars", [])
    }
    
    # Set default XPaths if not provided.
    if field_xpaths is None:
        field_xpaths = {"CarModel": "CarModel", "CarColor": "CarColor"}
    
    # Initialize counts for each feature.
    feature_counts = {
        "CarModel": {"up_to_date": 0, "total": 0},
        "CarColor": {"up_to_date": 0, "total": 0}
    }
    
    file_details = {}
    total_files = 0

    for filename in os.listdir(xml_folder):
        if filename.lower().endswith(".xml"):
            total_files += 1
            xml_path = os.path.join(xml_folder, filename)
            try:
                root = ET.parse(xml_path).getroot()
            except ET.ParseError as e:
                file_details[filename] = {"error": f"XML parse error: {e}"}
                continue
            
            # Extract features using provided XPaths.
            car_model_elem = root.find(field_xpaths.get("CarModel", "CarModel"))
            car_color_elem = root.find(field_xpaths.get("CarColor", "CarColor"))
            
            car_model = car_model_elem.text.strip() if car_model_elem is not None and car_model_elem.text else ""
            car_color = car_color_elem.text.strip() if car_color_elem is not None and car_color_elem.text else ""
            
            # Check whether the extracted values are up-to-date.
            model_current = 1 if car_model in up_to_date_values.get("CarModel", []) else 0
            # Compare CarColor case-insensitively.
            new_colors = [c.lower() for c in up_to_date_values.get("CarColor", [])]
            color_current = 1 if car_color.lower() in new_colors else 0
            
            # Update aggregated counts.
            feature_counts["CarModel"]["total"] += 1
            feature_counts["CarColor"]["total"] += 1
            if model_current:
                feature_counts["CarModel"]["up_to_date"] += 1
            if color_current:
                feature_counts["CarColor"]["up_to_date"] += 1
            
            overall_score = (model_current + color_current) / 2.0
            
            file_details[filename] = {
                "CarModel": car_model,
                "CarModel_current": model_current,
                "CarColor": car_color,
                "CarColor_current": color_current,
                "Feature_currentness_file": overall_score
            }
    
    # Calculate precision for each feature.
    features_results = {}
    for feature, counts in feature_counts.items():
        total = counts["total"]
        up_to_date = counts["up_to_date"]
        precision = up_to_date / total if total > 0 else 0
        features_results[feature] = {
            "up_to_date": up_to_date,
            "total": total,
            "precision": precision
        }
    
    overall_feature_currentness = (
        (features_results["CarModel"]["precision"] + features_results["CarColor"]["precision"]) / 2.0
        if total_files > 0 else 0
    )

    # Combine final results, excluding "features" and "total_files".
    results = {
        "file_details": file_details,
        "overall_feature_currentness": overall_feature_currentness
    }

    return json.dumps(results, ensure_ascii=False, indent=4)

# --- Example Usage ---
# if __name__ == "__main__":
#     xml_folder = "/home/reza/Desktop/data-validation/evaluation_license_plate_data/assets/xml"  # Update with your folder path.
#     field_xpaths = {"CarModel": "CarModel", "CarColor": "CarColor"}
#     report = FeatureCurrentness(xml_folder, field_xpaths)
#     print(json.dumps(report, ensure_ascii=False, indent=4))


#output 


    # {
    #     "file_details": {
    #         "1000423.xml": {
    #             "CarModel": "Peugeot-405",
    #             "CarModel_current": 1,
    #             "CarColor": "green",
    #             "CarColor_current": 0,
    #             "Feature_currentness_file": 0.5
    #         },
    #         "1000393.xml": {
    #             "CarModel": "Peugeot-405",
    #             "CarModel_current": 1,
    #             "CarColor": "grey",
    #             "CarColor_current": 0,
    #             "Feature_currentness_file": 0.5
    #         },
    #         "1000376.xml": {
    #             "CarModel": "Peugeot-207i",
    #             "CarModel_current": 0,
    #             "CarColor": "white",
    #             "CarColor_current": 1,
    #             "Feature_currentness_file": 0.5
    #         },
    #         "1000396.xml": {
    #             "CarModel": "Unknown",
    #             "CarModel_current": 0,
    #             "CarColor": "green",
    #             "CarColor_current": 0,
    #             "Feature_currentness_file": 0.0
    #         },
    #         "1000395.xml": {
    #             "CarModel": "Peugeot-405",
    #             "CarModel_current": 1,
    #             "CarColor": "silver",
    #             "CarColor_current": 1,
    #             "Feature_currentness_file": 1.0
    #         },
    #         "1000212.xml": {
    #             "CarModel": "Peugeot-206",
    #             "CarModel_current": 0,
    #             "CarColor": "No car detected",
    #             "CarColor_current": 0,
    #             "Feature_currentness_file": 0.0
    #         },
    #         "1000229.xml": {
    #             "CarModel": "Pride-131",
    #             "CarModel_current": 0,
    #             "CarColor": "red",
    #             "CarColor_current": 1,
    #             "Feature_currentness_file": 0.5
    #         },
    #         "1000244.xml": {
    #             "CarModel": "Peugeot-207i",
    #             "CarModel_current": 0,
    #             "CarColor": "white",
    #             "CarColor_current": 1,
    #             "Feature_currentness_file": 0.5
    #         },
    #         "1000211.xml": {
    #             "CarModel": "Peugeot-pars",
    #             "CarModel_current": 0,
    #             "CarColor": "white",
    #             "CarColor_current": 1,
    #             "Feature_currentness_file": 0.5
    #         },
    #         "1000198.xml": {
    #             "CarModel": "Peugeot-405",
    #             "CarModel_current": 1,
    #             "CarColor": "silver",
    #             "CarColor_current": 1,
    #             "Feature_currentness_file": 1.0
    #         }
    #     },
    #     "overall_feature_currentness": 0.5
    # }