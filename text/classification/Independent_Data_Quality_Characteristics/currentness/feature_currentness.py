"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd


def feature_currentness(df : pd.DataFrame, lable_col ,age_col='age', threshold_days=180) -> dict:
    """
    This function calculates the currentness of features in the dataset based on the 'age' column.
    It compares the 'age' column with a threshold value and determines the proportion of features
    that are recent (within the threshold) and outdated.

    :param df: The DataFrame containing the data.
    :param age_col: The name of the column containing the age in days (default is 'age').
    :param threshold_days: The number of days used to determine if a feature is recent (default is 180 days).
    :return: A dictionary containing the currentness of features and outdated feature records.
    """
    # Filter out recent data based on the age column, where age is less than or equal to the threshold
    recent_data = df[df[age_col] <= threshold_days]
    
    # Count the sentiment occurrences for all data and for recent data
    total_counts = df[lable_col].value_counts()  # Count occurrences of predicted sentiment in all data
    recent_counts = recent_data[lable_col].value_counts()  

    outdated_data = df[df[age_col] > threshold_days]  

    return {
        "feature_currentness": (recent_counts / total_counts).fillna(0).to_dict(), 
        "outdated_feature_rows": outdated_data.to_dict(orient='records') 
    }