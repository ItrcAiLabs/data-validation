import os
import json
import xml.etree.ElementTree as ET

# Mapping of province names to their possible codes
province_codes = {
    "East Azerbaijan": [15, 25, 35],
    "West Azerbaijan": [17, 27, 37],
    "Ardabil": [91],
    "Isfahan": [13, 23, 43, 53, 67],
    "Alborz": [68, 78, 21, 38, 30],
    "Ilam": [98],
    "Bushehr": [48, 58],
    "Tehran": [11, 22, 33, 44, 55, 66, 77, 88, 99, 10, 20, 40],
    "Chaharmahal and Bakhtiari": [71, 81],
    "South Khorasan": [32, 52],
    "Razavi Khorasan": [12, 32, 42, 36, 74],
    "North Khorasan": [32, 26],
    "Khuzestan": [14, 24, 34],
    "Zanjan": [87, 97],
    "Semnan": [86, 96],
    "Sistan and Baluchestan": [85, 95],
    "Fars": [63, 73, 83, 93],
    "Qazvin": [79, 89],
    "Qom": [16],
    "Kurdistan": [51, 61],
    "Kerman": [45, 65, 75],
    "Kermanshah": [19, 29],
    "Kohgiluyeh and Boyer-Ahmad": [49],
    "Golestan": [59, 69],
    "Gilan": [46, 56, 76],
    "Lorestan": [31, 41],
    "Mazandaran": [62, 72, 82, 92],
    "Markazi": [47, 57],
    "Hormozgan": [84, 94],
    "Hamedan": [18, 28],
    "Yazd": [54, 64, 74]
}

def get_province_name(code_str):
    """
    Given a province code as a string, convert it to an integer and return the corresponding
    province name from the province_codes dictionary. If the code doesn't match any province,
    the original code string is returned.
    """
    try:
        code_int = int(code_str)
    except ValueError:
        return code_str

    # Loop over province_codes to find a match; if a code appears in multiple provinces,
    # the first match is returned.
    for province, codes in province_codes.items():
        if code_int in codes:
            return province
    return code_str

def DataValueDistribution(xml_folder, xml_config):
    """
    Count the occurrences of each unique value for each field across all XML files.
    For the 'province_code' field, the code is replaced with the corresponding province name.
    
    Args:
        xml_folder (str): Path to the folder containing XML files.
        xml_config (dict): Dictionary mapping field names to XML paths.
    
    Returns:
        str: A JSON-formatted string representing a dictionary where each key is a field name and
             the value is another dictionary mapping each unique field value to its count.
    """


    features = {key: xml_config[key] for key in xml_config if key in {
                                                                                "car_model",
                                                                                "car_color",
                                                                                "series_letter",
                                                                                "province_code",
                                                                                }}
    # Initialize frequency dictionary for each field
    counts = {field: {} for field in features.keys()}
    
    # List all XML files in the given folder
    xml_files = [f for f in os.listdir(xml_folder) if f.endswith('.xml')]
    
    # Process each XML file
    for xml_file in xml_files:
        full_path = os.path.join(xml_folder, xml_file)
        try:
            tree = ET.parse(full_path)
            root = tree.getroot()
            
            # Process each field defined in xml_config
            for field, path in features.items():
                elements = root.findall(path)
                for element in elements:
                    if element.text and element.text.strip():
                        value = element.text.strip()
                        # For the province_code field, map the code to the province name
                        if field == "province_code":
                            value = get_province_name(value)
                        counts[field][value] = counts[field].get(value, 0) + 1
        except ET.ParseError:
            print(f"Warning: Could not parse {xml_file}, skipping.")
    
    return json.dumps(counts, ensure_ascii=False, indent=4)

