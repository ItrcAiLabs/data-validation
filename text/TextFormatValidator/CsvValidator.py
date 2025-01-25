import pandas as pd
from langdetect import detect

def validate_csv(file_path, text_columns, max_length=None, language=None):
    issues = []
    summary = {
        "total_rows": 0,
        "issues_count": 0,
        "max_length_violations": 0,
        "non_string_violations": 0,
        "none_value_violations": 0,
        "language_violations": 0
    }

    df = pd.read_csv(file_path)
    summary["total_rows"] = df.shape[0]  # Total rows in the CSV file
    
    # Loop through the specified text columns
    for col in text_columns:
        if col in df.columns:
            for row_num, value in enumerate(df[col], start=1):
                if pd.isna(value) or value == "":  # Check for None or empty values
                    issues.append({"row": row_num, "column": col, "error": "None or empty value"})
                    summary["none_value_violations"] += 1
                elif not isinstance(value, str):  # Check if the value is not a string
                    issues.append({"row": row_num, "column": col, "error": f"Non-string value: {value}"})
                    summary["non_string_violations"] += 1
                elif max_length and len(value) > max_length:  # Check for max length violations
                    issues.append({"row": row_num, "column": col, "error": f"Exceeds max length: {value}"})
                    summary["max_length_violations"] += 1
                elif language and detect(value) != language:  # Check for language mismatch
                    issues.append({"row": row_num, "column": col, "error": f"Language mismatch: Expected {language}, got {detect(value)}"})
                    summary["language_violations"] += 1

    summary["issues_count"] = len(issues)
    return summary, issues