"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd
import json

def data_format_consistency(df: pd.DataFrame, expected_formats: dict) -> str:
    """
    Check the consistency of data formats across columns and return the results in JSON format.
    
    Parameters:
    - df: DataFrame containing the data.
    - expected_formats: Dictionary specifying the expected data types for each column.
    
    Returns:
    - A JSON string containing the ratio of columns with consistent data formats 
      and rows with inconsistent formats.
    """
    inconsistent_rows = []

    for col, expected_type in expected_formats.items():
        if col in df.columns:
            if expected_type == 'datetime':
                inconsistent_mask = ~pd.to_datetime(df[col], errors='coerce').notna()
            else:
                inconsistent_mask = ~df[col].apply(lambda x: isinstance(x, expected_type))
            
            inconsistent_rows.append(df[inconsistent_mask])

    # Concatenate all inconsistent rows and drop duplicates
    if inconsistent_rows:
        inconsistent_df = pd.concat(inconsistent_rows).drop_duplicates()
    else:
        inconsistent_df = pd.DataFrame()

    # Calculate format consistency ratio
    consistent_columns = sum(df[col].apply(lambda x: all(isinstance(i, expected_formats[col]) 
                                                          if expected_formats[col] != 'datetime' 
                                                          else pd.to_datetime(i, errors='coerce') is not pd.NaT 
                                                          for i in x)) for col in expected_formats)
    
    ratio = consistent_columns / len(expected_formats)

    result = {
        "format_consistency_ratio": ratio,
        "inconsistent_rows": inconsistent_df.to_dict(orient='records')  # Convert to list of dictionaries
    }

    return json.dumps(result, ensure_ascii=False, indent=4)





