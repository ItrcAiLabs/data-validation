import json
import pandas as pd

def accuracy_assurance(df: pd.DataFrame, text_column: str = 'text', label_column: str = 'label') -> str:
    """
    Calculate the data accuracy assurance (coverage of validated data) and return detailed results in JSON format.
    
    Parameters:
    - df: DataFrame containing the data.
    - text_column: Name of the column containing the text.
    - label_column: Name of the column containing the label.
    
    Returns:
    - A JSON string containing data accuracy assurance and a summary of invalid rows.
    """
    # Identify validated records (non-null text and label)
    validated_data = df[(df[text_column].notnull()) & (df[label_column].notnull())]
    
    # Identify invalid records (either text or label is null)
    invalid_data = df[(df[text_column].isnull()) | (df[label_column].isnull())]
    
    # Calculate data accuracy assurance
    assurance = len(validated_data) / len(df) if len(df) > 0 else 0

    # Prepare the result as a dictionary
    result = {
        "data_accuracy_assurance": assurance,
        "Wrong Data": invalid_data.to_dict(orient='records')  # Convert invalid rows to a list of dictionaries
    }

    # Convert the result to a JSON string and return
    return json.dumps(result, ensure_ascii=False, indent=4)
