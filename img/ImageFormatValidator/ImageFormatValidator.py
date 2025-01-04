from .utils import * 



def ImageFormatValidator(list_path_images : list, 
                         list_images : list, 
                         max_size_mb : float, 
                         allowed_formats : list, 
                         min_size_mb : float, 
                         expected_dimensions_list : list, 
                         expected_mode : str, 
                         pixel_range : tuple) -> list:
    validation_results = []

    for image_path in list_path_images:
        report = {"image_path": image_path, "status": []}

        # Check file exists
        check_point, report_text = check_file_exists(image_path, list_images)
        report["status"].append({"file_exists": check_point, "message": report_text})

        # Check file size
        check_point, report_text = check_file_size(image_path, max_size_mb, min_size_mb)
        report["status"].append({"file_size": check_point, "message": report_text})

        # Check file format
        check_point, report_text = check_file_format(image_path, allowed_formats)
        report["status"].append({"file_format": check_point, "message": report_text})

        # Check image dimensions
        check_point, report_text = check_image_dimensions(image_path, expected_dimensions_list)
        report["status"].append({"image_dimensions": check_point, "message": report_text})

        # Check file structure
        check_point, report_text = check_file_structure(image_path)
        report["status"].append({"file_structure": check_point, "message": report_text})

        # Check pixel data
        check_point, report_text = check_pixel_data(image_path, expected_mode, pixel_range)
        report["status"].append({"pixel_data": check_point, "message": report_text})

        validation_results.append(report)

    return validation_results
