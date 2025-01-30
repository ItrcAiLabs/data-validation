import pandas as pd
from datetime import datetime

def calculate_age(df, timestamp_col='timestamp'):
    """
    Calculates the age of data based on the timestamp column.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        timestamp_col (str): Name of the timestamp column (default: 'timestamp').
    
    Returns:
        pd.DataFrame: DataFrame with a new column 'age' indicating the age of the data.
    """
    # Convert the timestamp column to datetime format
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Calculate the age of the data (difference between current time and the timestamp)
    current_time = datetime.now()
    df['age'] = (current_time - df[timestamp_col]).dt.days
    
    return df