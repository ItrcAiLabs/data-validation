import json
import pandas as pd

def risk_of_inaccuracy(df: pd.DataFrame, text_column: str = 'text', min_length: int = 5, max_length: int = 500) -> str:
    """
    Calculate the risk of dataset inaccuracy (ratio of outlier texts) and return the results in JSON format.

    Parameters:
    - df: DataFrame containing the data.
    - text_column: Name of the column containing the text.
    - min_length: Minimum allowed text length.
    - max_length: Maximum allowed text length.

    Returns:
    - A JSON string containing the risk of inaccuracy and the original text rows that are outliers.
    """
    # Calculate the length of texts
    df['text_length'] = df[text_column].apply(len)
    
    # Identify outlier texts
    outliers = df[(df['text_length'] < min_length) | (df['text_length'] > max_length)]
    
    # Calculate the risk of inaccuracy
    risk = len(outliers) / len(df)
    
    # Prepare the output as a dictionary to be converted to JSON
    result = {
        "risk_of_inaccuracy": risk,
        "Wrong Data": outliers[text_column].tolist()  # Convert outlier rows to a list
    }
    
    # Convert the result to a JSON string and return
    return json.dumps(result, ensure_ascii=False, indent=4)
