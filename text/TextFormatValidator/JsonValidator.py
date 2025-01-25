import json
from langdetect import detect

def validate_json(file_path, text_keys, max_length=None, language=None):
    """
    Validates text fields in a JSON file and generates a summary report.
    :param file_path: Path to the JSON file.
    :param text_keys: List of keys to validate as text.
    :param max_length: Maximum length allowed for text data (optional).
    :param language: Expected language code (optional).
    """
    issues = []
    summary = {
        "total_objects": 0,
        "issues_count": 0,
        "max_length_violations": 0,
        "non_string_violations": 0,
        "none_value_violations": 0,
        "language_violations": 0
    }

    with open(file_path, 'r') as jsonfile:
        data = json.load(jsonfile)
        summary["total_objects"] = len(data)

        for obj_num, obj in enumerate(data, start=1):
            for key in text_keys:
                if key in obj:
                    value = obj[key]
                    if value is None or value == "":
                        issues.append({"object": obj_num, "key": key, "error": "None or empty value"})
                        summary["none_value_violations"] += 1
                    elif not isinstance(value, str):
                        issues.append({"object": obj_num, "key": key, "error": f"Non-string value: {value}"})
                        summary["non_string_violations"] += 1
                    elif max_length and len(value) > max_length:
                        issues.append({"object": obj_num, "key": key, "error": f"Exceeds max length: {value}"})
                        summary["max_length_violations"] += 1
                    elif language and detect(value) != language:
                        issues.append({"object": obj_num, "key": key, "error": f"Language mismatch: Expected {language}, got {detect(value)}"})
                        summary["language_violations"] += 1

    summary["issues_count"] = len(issues)
    return summary, issues