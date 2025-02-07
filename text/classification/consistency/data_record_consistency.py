"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""


import pandas as pd
import json

class DataRecordConsistency:
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Class to evaluate the consistency of records by checking for duplicate entries in the dataset.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        """
        self.df = df
        self.duplicate_records = pd.DataFrame()
        self.duplicate_record_ratio = 0.0
    
    def evaluate_consistency(self) -> None:
        """
        Identifies duplicate records and calculates the ratio of duplicate records in the dataset.
        """
        self.duplicate_records = self.df[self.df.duplicated()]
        self.duplicate_record_ratio = len(self.duplicate_records) / len(self.df) if len(self.df) > 0 else 0.0
    
    def get_consistency_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing the duplicate record ratio and the list of duplicate rows.
        
        Returns:
        - A JSON string containing the duplicate record ratio and the duplicate rows.
        """
        result = {
            "duplicate_record_ratio": self.duplicate_record_ratio,
            "duplicate_rows": self.duplicate_records.to_dict(orient='records')  # Convert duplicate rows to a list of dictionaries
        }
        return json.dumps(result, ensure_ascii=False, indent=4)


# Example usage (Farsi Sentiment Dataset)
# data = {
#     "text": [
#         "این یک محصول عالی است",  # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#         "خرید این محصول را پیشنهاد نمی‌کنم",  # Negative
#         "این یک محصول عالی است"  # Positive (duplicate)
#     ],
#     "label": ["مثبت", "منفی", "خنثی", "منفی", "مثبت"],  # Labels for the sentiment
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-01"]
# }
# df = pd.DataFrame(data)

# # Data record consistency check
# consistency_checker = DataRecordConsistency(df)
# consistency_checker.evaluate_consistency()
# print(consistency_checker.get_consistency_report())

# Output:
# {
#     "duplicate_record_ratio": 0.2,
#     "duplicate_rows": [
#         {
#             "text": "این یک محصول عالی است",
#             "label": "مثبت",
#             "date": "2024-01-05"
#         }
#     ]
# }
