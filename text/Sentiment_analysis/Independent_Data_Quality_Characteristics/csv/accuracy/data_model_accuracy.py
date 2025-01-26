def data_model_accuracy(df, text_column: str = 'text', label_column: str = 'label') -> dict:
    """
    Calculate the data model accuracy (alignment of data structure with requirements) and provide detailed feedback.
    
    Parameters:
    - df: DataFrame containing the data.
    - text_column: Name of the column containing the text.
    - label_column: Name of the column containing the label.
    
    Returns:
    - A dictionary with:
        - `accuracy`: Data model accuracy as a value between 0 and 1.
        - `missing_columns`: A list of required columns that are missing.
    """
    # Check if required columns exist
    required_columns = [text_column, label_column]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    # Calculate accuracy
    accuracy = 1.0 if not missing_columns else 0.0
    
    # Return detailed result
    return {
        "accuracy": accuracy,
        "missing_columns": missing_columns
    }
