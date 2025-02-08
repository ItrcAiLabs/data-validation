"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import json
import pandas as pd


class FeatureCompleteness:
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Class to evaluate the completeness of features by checking for missing values column-wise.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        """
        self.df = df
        self.missing_features = {}
        self.completeness_scores = {}
    
    def evaluate_completeness(self) -> None:
        """
        Calculates feature completeness percentages and identifies missing features.
        """
        self.missing_features = self.df.isnull().sum()[self.df.isnull().sum() > 0].to_dict()
        self.completeness_scores = (self.df.notnull().sum() / len(self.df)).to_dict()
    
    def get_completeness_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing feature completeness.
        
        Returns:
        - A JSON string containing completeness percentages and missing features.
        """
        result = {
            "feature_completeness": self.completeness_scores,
            "missing_features": self.missing_features  # List of features with missing values
        }
        return json.dumps(result, ensure_ascii=False, indent=4)


# Example usage (Farsi Sentiment Dataset)
# data = {
#     "text": [
#         "این یک محصول عالی است",  # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#         None  # Missing value
#     ],
#     "label": ["مثبت", "منفی", "خنثی", None],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
# }
# df = pd.DataFrame(data)

# completeness_checker = FeatureCompleteness(df)
# completeness_checker.evaluate_completeness()
# print(completeness_checker.get_completeness_report())

# Output:
# {
#     "feature_completeness": {
#         "text": 0.75,
#         "label": 0.75,
#         "date": 1.0
#     },
#     "missing_features": {
#         "text": 1,
#         "label": 1
#     }
# }