"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd

def record_currentness_based_on_age(df : pd.DataFrame, age_col='age', threshold_days=180) -> dict:
    """
    This function calculates the currentness of records in the dataset based on the 'age' column.
    It determines the proportion of records that are recent (within the threshold) and outdated.

    :param df: The DataFrame containing the data.
    :param age_col: The name of the column containing the age in days (default is 'age').
    :param threshold_days: The number of days used to determine if a record is recent (default is 180 days).
    :return: A dictionary containing the currentness of records and outdated record rows.
    """
    # Filter out recent records based on the age column, where age is less than or equal to the threshold
    recent_records = df[df[age_col] <= threshold_days]
    
    # Filter records that are outdated, where age is greater than the threshold
    outdated_records = df[df[age_col] > threshold_days]

    return {
        "record_currentness": len(recent_records) / len(df) if len(df) > 0 else 0,  # Calculate the proportion of recent records
        "outdated_records": outdated_records.to_dict(orient='records')  # Convert outdated records to a dictionary format
    }
