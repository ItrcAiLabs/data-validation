"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import json
import pandas as pd


class DataModelAccuracy:
    def __init__(self, df: pd.DataFrame, required_columns: list, required_size: int) -> None:
        """
        Class to calculate data model accuracy by validating the alignment of data structure with requirements.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        - required_columns: List of required column names that should be present in the dataset.
        - required_size: Minimum required number of rows in the dataset.
        """
        self.df = df
        self.required_columns = required_columns
        self.required_size = required_size
        
        self.missing_columns = []
        self.accuracy_scores = {}
    
    def check_columns(self) -> float:
        """
        Check if all required columns exist in the DataFrame.
        
        Returns:
        - Accuracy score based on the presence of required columns.
        """
        self.missing_columns = [col for col in self.required_columns if col not in self.df.columns]
        accuracy = 1 - (len(self.missing_columns) / len(self.required_columns))
        self.accuracy_scores['column_presence'] = accuracy
        return accuracy

    def check_rows(self) -> float:
        """
        Check if the dataset meets the required minimum size.
        
        Returns:
        - Accuracy score based on whether the dataset size requirement is met.
        """
        accuracy = 1.0 if len(self.df) >= self.required_size else len(self.df) / self.required_size
        self.accuracy_scores['size_requirement'] = accuracy
        return accuracy
    
    def calculate_overall_accuracy(self) -> float:
        """
        Calculate the overall accuracy by averaging the individual accuracy scores.
        
        Returns:
        - A float value representing the mean accuracy of all checks performed.
        """
        return sum(self.accuracy_scores.values()) / len(self.accuracy_scores) if self.accuracy_scores else 0
    
    def get_model_accuracy(self) -> str:
        """
        Generate a JSON-formatted report containing accuracy scores, overall accuracy, and missing columns.
        
        Returns:
        - A JSON string summarizing the accuracy assessment.
        """
        result = {
            "accuracy_scores": self.accuracy_scores,
            "overall_accuracy": self.calculate_overall_accuracy(),
            "missing_columns": self.missing_columns  # List of missing columns
        }
        return json.dumps(result, ensure_ascii=False, indent=4)

# # Example usage
# Example usage (Farsi Sentiment Dataset)
# data = {
#     "text": [
#         "این یک محصول عالی است",  # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#     ],
#     "label": ["مثبت", "منفی", "خنثی"],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03"]
# }
# df = pd.DataFrame(data)
# required_columns = ["text", "label", "date", "id"]
# required_size = 5

# model_accuracy = DataModelAccuracy(df, required_columns, required_size)
# model_accuracy.check_columns()
# model_accuracy.check_rows()
# print(model_accuracy.get_model_accuracy())


# output : 

    # {
    #     "accuracy_scores": {
    #         "column_presence": 0.75,
    #         "size_requirement": 0.6
    #     },
    #     "overall_accuracy": 0.675,
    #     "missing_columns": [
    #         "id"
    #     ]
    # }