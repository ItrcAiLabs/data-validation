import os
import json

def DataRecordConsistency(image_folder, xml_folder):
    # Define valid image extensions (case-insensitive)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    
    # List image files
    image_files = [f for f in os.listdir(image_folder) 
                   if os.path.splitext(f)[1].lower() in image_extensions]
    
    # List XML files
    xml_files = [f for f in os.listdir(xml_folder) 
                 if os.path.splitext(f)[1].lower() == '.xml']
    
    # Extract base names
    xml_base_names = {os.path.splitext(f)[0] for f in xml_files}
    image_base_names = {os.path.splitext(f)[0] for f in image_files}
    
    # Find images with and without XML matches
    images_with_xml = [f for f in image_files if os.path.splitext(f)[0] in xml_base_names]
    images_without_xml = [f for f in image_files if os.path.splitext(f)[0] not in xml_base_names]
    
    # Find XML files without image matches
    xml_without_images = [f for f in xml_files if os.path.splitext(f)[0] not in image_base_names]
    
    # Calculate consistency score
    total_images = len(image_files)
    score = len(images_with_xml) / total_images if total_images > 0 else 0.0
    
    # Construct the report
    report = {
        "summary": {
            "consistency_score": score
        },
        "errors": {
            "images_without_xml": images_without_xml,
            "xml_without_images": xml_without_images
        }
    }
    
    return json.dumps(report, ensure_ascii=False, indent=4)

