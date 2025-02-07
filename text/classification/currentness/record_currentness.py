"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import pandas as pd
from datetime import datetime
from utils import *


class RecordCurrentness:
    def __init__(self, df: pd.DataFrame, timestamp_col='timestamp', threshold_days=180):
        """
        Initializes the RecordCurrentness class to evaluate the currentness of records.

        :param df: The DataFrame containing the data.
        :param timestamp_col: The name of the column containing the timestamp (default is 'timestamp').
        :param threshold_days: The number of days used to determine if a record is recent (default is 180 days).
        """
        self.df = df
        self.timestamp_col = timestamp_col
        self.threshold_days = threshold_days
        self.record_currentness = 0
        self.outdated_records = []

    def calculate_age(self):
        """
        Calculate the 'age' of each record based on the timestamp.
        Adds a new column 'age' to the DataFrame.
        """
        self.df = calculate_age(self.df, self.timestamp_col)

    def evaluate_currentness(self):
        """
        This function calculates the currentness of records in the dataset based on the 'age' column,
        which is calculated based on the 'timestamp' column. It determines the proportion of records 
        that are recent (within the threshold) and outdated.
        """
        # First, calculate the age based on the timestamp column
        self.calculate_age()

        # Filter out recent records based on the age column, where age is less than or equal to the threshold
        recent_records = self.df[self.df['age'] <= self.threshold_days]

        # Filter records that are outdated, where age is greater than the threshold
        self.outdated_records = self.df[self.df['age'] > self.threshold_days]

        # Calculate the proportion of recent records
        self.record_currentness = len(recent_records) / len(self.df) if len(self.df) > 0 else 0

    def get_currentness_report(self) -> dict:
        """
        Generate a dictionary containing the record currentness ratio and outdated records.

        :return: A dictionary containing the currentness ratio and outdated record rows.
        """
        return {
            "record_currentness": self.record_currentness,
            "outdated_records": self.outdated_records.to_dict(orient='records')
        }


# Example usage
# Sample DataFrame with timestamp data
# data = {
#     "text": [
#         "این یک محصول عالی است",  # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#         "خرید این محصول را پیشنهاد نمی‌کنم",  # Negative
#     ],
#     "timestamp": ["2024-01-01", "2023-07-15", "2022-06-01", "2023-11-10"],  # Timestamps for each record
# }
# df = pd.DataFrame(data)

# # Record currentness check
# currentness_checker = RecordCurrentness(df, threshold_days=600)
# currentness_checker.evaluate_currentness()
# result = currentness_checker.get_currentness_report()
# print(result)


# Example Output:


# {
#     "record_currentness": 0.75,
#     "outdated_records": [
#         {
#             "text": "محصول متوسط بود، می‌توانست بهتر باشد",
#             "timestamp": "2022-06-01",
#             "age": 588
#         }
#     ]
# }