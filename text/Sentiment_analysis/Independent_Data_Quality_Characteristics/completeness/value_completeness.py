"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.

    data validation tools : value_completeness
    Authors: ALireza Parvaresh
    Contributors: mojgan farhoudi , mohmmad hadi bokaei
    URL: <https://itrc.ac.ir/fa/>
    For license information, see LICENSE.TXT
"""
import pandas as pd
import json

def value_completeness(df : pd.DataFrame) -> str:
    """
    Calculates the proportion of missing values in the dataset and identifies rows with missing values.

    Parameters:
    - df (DataFrame): The dataset to analyze.

    Returns:
    - JSON string: Contains completeness ratio and missing rows.
    """
    missing_values = df[df.isnull().any(axis=1)]  # Identify rows with missing values
    return json.dumps({
        "value_completeness": df.notnull().sum().sum() / df.size,  # Ratio of available data
        "missing_rows": missing_values.to_dict(orient='records')  # List of rows with missing values
    }, ensure_ascii=False, indent=4)
