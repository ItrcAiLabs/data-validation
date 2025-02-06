"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import pandas as pd
import json

def data_record_consistency(df: pd.DataFrame) -> str:
    """
    Calculate the ratio of duplicate records in the dataset and return the results in JSON format.
    
    Parameters:
    - df: DataFrame containing the data.
    
    Returns:
    - A JSON string containing the ratio of duplicate records and the duplicate rows.
    """
    # Identify duplicate records
    duplicate_records = df[df.duplicated()]
    
    # Calculate the ratio of duplicate records
    ratio = len(duplicate_records) / len(df)
    
    # Prepare the output as a dictionary to be converted to JSON
    result = {
        "duplicate_record_ratio": ratio,
        "duplicate_rows": duplicate_records.to_dict(orient='records')  # Convert duplicate rows to a list of dictionaries
    }
    
    # Convert the result to a JSON string and return
    return json.dumps(result, ensure_ascii=False, indent=4)