"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import pandas as pd
import re
import json
import .utils * 

def validate_text(text: str, sequence_of_operations: list) -> str:
    """Validate and process the text based on the sequence of operations."""
    # Apply all operations in sequence
    for operation in sequence_of_operations:
        if operation == "remove_mentions":
            # Remove mentions (e.g., @username) using a regex pattern
            text = re.sub(r'@\w+', '', text)  # Remove all mentions starting with '@'
        elif operation == "remove_links":
            text = re.sub(r'http\S+', '', text)  # Remove links
        elif operation == "remove_persian_punctuations":
            text = remove_persian_punctuation(text)  # Remove Persian punctuations
        elif operation == "remove_stopwords":
            text = remove_stopwords(text)  # Remove stopwords
        elif operation == "remove_arabic_diacritics":
            text = remove_arabic_diacritics(text)  # Remove Arabic diacritics
        elif operation == "spell_check":
            text = remove_not_corrected_spell(text) # remove text not correected text
        elif operation == "remove_informal_words":
            text = remove_informal_words(text)  # remove informal words
    
    # Remove invalid characters after applying operations
    return text.strip()

def syntactic_accuracy(df: pd.DataFrame, text_column='text', sequence_of_operations: list = None) -> str:
    """
    Calculate the syntactic accuracy of texts in the dataset and return the problematic text rows in JSON format.

    Parameters:
    - df: DataFrame containing the data.
    - text_column: Name of the column containing the text.
    - sequence_of_operations: List of operations to be applied (optional, not yet used in this version).

    Returns:
    - A JSON string containing syntactic accuracy and the original text rows with problems.
    """

    
    # Validate the format of the text
    df['cleaned_text'] = df[text_column].apply(validate_text)
    
    # Calculate syntactic accuracy (1 for valid, 0 for invalid)
    accuracy = df['cleaned_text'].apply(lambda x: 1 if x else 0).mean()
    
    # Identify problematic rows (where cleaned text is empty or invalid)
    problematic_rows = df[df['cleaned_text'] == ""]
    
    # Prepare the output as a dictionary to be converted to JSON
    result = {
        "accuracy": accuracy,
        "Wrong Data": problematic_rows[text_column].tolist()  # Convert the problematic rows to a list
    }
    
    # Convert the result to a JSON string and return
    return json.dumps(result, ensure_ascii=False, indent=4)

