"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import pandas as pd
import json

def semantic_consistency(df: pd.DataFrame, label_column: str = 'label', valid_labels: set = {'positive', 'negative', 'neutral'}) -> str:
    """
    Check the semantic consistency of labels in the dataset and return the results in JSON format.
    
    Parameters:
    - df: DataFrame containing the data.
    - label_column: Name of the label column (default is 'label').
    - valid_labels: Set of valid labels (default is {'positive', 'negative', 'neutral'}).
    
    Returns:
    - A JSON string containing the ratio of valid labels and rows with invalid labels.
    """
    # Check if labels are in the set of valid labels
    invalid_rows = df[~df[label_column].isin(valid_labels)]
    
    # Calculate the ratio of valid labels
    ratio = (len(df) - len(invalid_rows)) / len(df)
    
    # Prepare the output as a dictionary to be converted to JSON
    result = {
        "semantic_consistency_ratio": ratio,
        "invalid_rows": invalid_rows.to_dict(orient='records')  # Convert invalid rows to a list of dictionaries
    }
    
    # Convert the result to a JSON string and return
    return json.dumps(result, ensure_ascii=False, indent=4)