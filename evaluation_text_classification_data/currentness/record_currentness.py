import pandas as pd
import json
from datetime import datetime
from .utils import *

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
        self.outdated_records = pd.DataFrame()  # Initialize as an empty DataFrame

    def calculate_age(self):
        """
        Calculate the 'age' of each record based on the timestamp.
        Adds a new column 'age' to the DataFrame.
        """
        self.df = calculate_age(self.df, self.timestamp_col)

    def evaluate_currentness(self):
        """
        Calculates the currentness of records in the dataset based on the 'age' column,
        which is calculated using the 'timestamp' column. It determines the proportion of records 
        that are recent (within the threshold) and stores outdated records.
        """
        self.calculate_age()
        recent_records = self.df[self.df['age'] <= self.threshold_days]
        self.outdated_records = self.df[self.df['age'] > self.threshold_days]
        self.record_currentness = len(recent_records) / len(self.df) if len(self.df) > 0 else 0

    def get_currentness_report(self) -> str:
        """
        Generate a JSON-formatted string containing the record currentness ratio and outdated records.

        :return: A JSON string with keys "record_currentness" and "outdated_records".
        """
        result =  {
            "record_currentness": self.record_currentness,
            "outdated_records": self.outdated_records.to_dict(orient='records')
        }
        return json.dumps(result, indent=4, ensure_ascii=False,  default=str)

# Example usage:
# data = {
#     "text": [
#         "این یک محصول عالی است",
#         "کیفیت خیلی بد بود، ناراضی هستم",
#         "محصول متوسط بود، می‌توانست بهتر باشد",
#         "خرید این محصول را پیشنهاد نمی‌کنم",
#     ],
#     "timestamp": ["2024-01-01", "2023-07-15", "2022-06-01", "2023-11-10"],
# }
# df = pd.DataFrame(data)
#
# currentness_checker = RecordCurrentness(df, threshold_days=600)
# currentness_checker.evaluate_currentness()
# result = currentness_checker.get_currentness_report()
# print(result)
