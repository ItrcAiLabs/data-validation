"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import json
import pandas as pd



class RecordCompleteness:
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Class to evaluate the completeness of records by checking the ratio of fully complete rows.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        """
        self.df = df
        self.record_completeness = 0.0
        self.records_with_missing_values = pd.DataFrame()
    
    def evaluate_record_completeness(self) -> None:
        """
        Calculates the ratio of complete records (no missing values) to the total records
        and identifies records with missing values.
        """
        self.record_completeness = (self.df.dropna().shape[0] / len(self.df)) if len(self.df) > 0 else 0.0
        self.records_with_missing_values = self.df[self.df.isnull().any(axis=1)]
    
    def get_record_completeness_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing record completeness and listing records with missing values.
        
        Returns:
        - A JSON string containing the record completeness ratio and records with missing values.
        """
        result = {
            "record_completeness": self.record_completeness,  # Ratio of records without missing values
            "records_with_missing_values": self.records_with_missing_values.to_dict(orient='records')
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
#     "label": ["مثبت",None, "خنثی", None],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
# }
# df = pd.DataFrame(data)


# # Record completeness check
# record_checker = RecordCompleteness(df)
# record_checker.evaluate_record_completeness()
# print(record_checker.get_record_completeness_report())

# Output:

    # {
    # "record_completeness": 0.5,
    # "records_with_missing_values": [
    #     {
    #         "text": "کیفیت خیلی بد بود، ناراضی هستم",
    #         "label": null,
    #         "date": "2024-01-02"
    #     },
    #     {
    #         "text": null,
    #         "label": null,
    #         "date": "2024-01-04"
    #     }
    # ]
    # }
