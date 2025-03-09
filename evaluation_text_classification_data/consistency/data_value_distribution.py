"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd
import json

class DataValueDistribution:
    def __init__(self, df: pd.DataFrame, label_column: str = 'label') -> None:
        """
        Class to analyze the distribution of labels in a dataset.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        - label_column: Name of the label column (default is 'label').
        """
        self.df = df
        self.label_column = label_column
        self.label_distribution = {}
    
    def analyze_distribution(self) -> None:
        """
        Analyzes the distribution of labels in the dataset.
        """
        # Calculate the distribution of labels
        self.label_distribution = self.df[self.label_column].value_counts().to_dict()
    
    def get_distribution_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing the label distribution.
        
        Returns:
        - A JSON string containing the distribution of labels.
        """
        result = {
            "label_distribution": self.label_distribution
        }
        return json.dumps(result, ensure_ascii=False, indent=4, default=str)

# Example usage
# data = {
#     "text": [
#         "این یک محصول عالی است",  # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#         "خرید این محصول را پیشنهاد نمی‌کنم",  # Negative
#     ],
#     "label": ["مثبت", "منفی", "خنثی", "منفی"],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
# }
# df = pd.DataFrame(data)

# # Data value distribution check
# distribution_checker = DataValueDistribution(df)
# distribution_checker.analyze_distribution()
# print(distribution_checker.get_distribution_report())

# Example Output:
# {
#     "label_distribution": {
#         "منفی": 2,
#         "مثبت": 1,
#         "خنثی": 1
#     }
# }
