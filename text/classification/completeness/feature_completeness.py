"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.

    data validation tools : feature completeness
    Authors: ALireza Parvaresh
    Contributors: mojgan farhoudi , mohmmad hadi bokaei
    URL: <https://itrc.ac.ir/fa/>
    For license information, see LICENSE.TXT
"""
import pandas as pd
import json


def feature_completeness(df : pd.DataFrame) -> str:
    """
    Evaluates the completeness of each feature by checking for missing values column-wise.

    Parameters:
    - df (DataFrame): The dataset to analyze.

    Returns:
    - JSON string: Contains feature completeness percentages and missing features.
    """
    missing_features = df.isnull().sum()[df.isnull().sum() > 0]  # Identify missing features
    return json.dumps({
        "feature_completeness": (df.notnull().sum() / len(df)).to_dict(),  # Completeness per feature
        "missing_features": missing_features.to_dict()  # List of features with missing values
    }, ensure_ascii=False, indent=4)
