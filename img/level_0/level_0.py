from utils import * 


def level_0(path_logger : str, 
            list_path_images : list, 
            list_images : list, 
            max_size_mb: int, 
            allowed_formats : list,
            min_size_mb: int, 
            expected_dimensions_list : list,
            expected_mode : str,
            pixel_range : tuple) -> None:
    

    file = open(path_logger, 'a')

    file.write("---This is a level zero photo data validation report" + "\n")  # Append content and add a new line at the end
    for image_path in list_path_images:

        file.write(f"{image_path}" + "\n")  

        # check file exists
        check_point, report_text = check_file_exists(image_path, list_images)
        if check_point:
            file.write(f" --- file exists ✔️" + "\n")
        if not check_point:
            file.write(f"--- file exists ❌ report{report_text} " + "\n")

        # check file size
        check_point, report_text = check_file_size(image_path, max_size_mb, min_size_mb)
        if check_point:
            file.write(f" --- file size ✔️" + "\n")
        if not check_point:
            file.write(f"--- file size ❌ report{report_text} " + "\n")



        # check check file format
        check_point, report_text = check_file_format(image_path, allowed_formats ) 
        if check_point:
            file.write(f" --- file format ✔️" + "\n")
        if not check_point:
            file.write(f"--- file format ❌ report{report_text} " + "\n")
        
        # check image dimensions
        check_point, report_text = check_image_dimensions(image_path , expected_dimensions_list)
        if check_point:
            file.write(f"--- image dimensions ✔️" + "\n")
        if not check_point:
            file.write(f"--- image dimensions ❌ report{report_text} " + "\n")


        # check file structure
        check_point, report_text = check_file_structure(image_path)
        if check_point:
            file.write(f"--- file structure ✔️" + "\n")
        if not check_point:
            file.write(f"--- file structure ❌ report{report_text} " + "\n")

        # check pixel data
        check_point, report_text = check_pixel_data(image_path, expected_mode, pixel_range)
        if check_point:
            file.write(f"--- pixel data ✔️" + "\n")
        if not check_point:
            file.write(f"--- pixel data ❌ report{report_text} " + "\n")
