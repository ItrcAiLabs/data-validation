"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import pandas as pd
import json

def data_value_distribution(df: pd.DataFrame, label_column: str = 'label') -> str:
    """
    Analyze the distribution of labels in the dataset and return the results in JSON format.
    
    Parameters:
    - df: DataFrame containing the data.
    - label_column: Name of the label column (default is 'label').
    
    Returns:
    - A JSON string containing the distribution of labels.
    """
    # Calculate the distribution of labels
    label_distribution = df[label_column].value_counts().to_dict()
    
    # Prepare the output as a dictionary to be converted to JSON
    result = {
        "label_distribution": label_distribution
    }
    
    # Convert the result to a JSON string and return
    return json.dumps(result, ensure_ascii=False, indent=4)