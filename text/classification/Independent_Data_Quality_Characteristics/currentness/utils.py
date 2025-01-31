import pandas as pd
from datetime import datetime

# Function to calculate age based on timestamp column
def calculate_age(df, timestamp_col='timestamp'):
    """
    This function calculates the 'age' of data records in days based on the timestamp.
    It adds an 'age' column to the DataFrame, where the age is calculated as the
    difference in days between the current date and the timestamp.

    :param df: The DataFrame containing the data.
    :param timestamp_col: The name of the column containing the timestamp (default is 'timestamp').
    :return: The DataFrame with an additional 'age' column.
    """
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])  
    current_time = datetime.now()  
    df['age'] = (current_time - df[timestamp_col]).dt.days  
    return df  