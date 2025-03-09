"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import json
import pandas as pd



class ValueOcurrenceCompletness:
    def __init__(self, df: pd.DataFrame, label_column: str, expected_occurrences: dict) -> None:
        """
        Class to calculate label accuracy based on the expected and actual occurrences of labels.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        - label_column: Column name containing the labels.
        - expected_occurrences: A dictionary where keys are labels and values are expected occurrences.
        """
        self.df = df
        self.label_column = label_column
        self.expected_occurrences = expected_occurrences
        self.label_accuracy = {}
        self.overall_accuracy = 0.0
    
    def evaluate_label_accuracy(self) -> None:
        """
        Calculates accuracy for each label and the overall accuracy based on expected occurrences provided by the user.
        """
        label_counts = self.df[self.label_column].value_counts().to_dict()
        
        self.label_accuracy = {
            label: min(1, self.expected_occurrences[label] / count)
            for label, count in label_counts.items() if label in self.expected_occurrences
        }

        self.overall_accuracy = sum(self.label_accuracy.values()) / len(self.label_accuracy) if self.label_accuracy else 0.0
    
    def get_label_accuracy_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing label accuracy.
        
        Returns:
        - A JSON string containing accuracy per label and overall accuracy.
        """
        result = {
            "label_accuracy": self.label_accuracy,
            "overall_accuracy": self.overall_accuracy
        }
        return json.dumps(result, ensure_ascii=False, indent=4)


# Example usage (Farsi Sentiment Dataset)
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

# # Define expected occurrences for each label
# expected_occurrences = {
#     "مثبت": 2,
#     "منفی": 2,
#     "خنثی": 1
# }


# # Label accuracy check
# label_checker = ValueOcurrenceCompletness(df, "label", expected_occurrences)
# label_checker.evaluate_label_accuracy()
# print(label_checker.get_label_accuracy_report())

# Output:
# {
#     "label_accuracy": {
#         "مثبت": 1.0,
#         "منفی": 1.0,
#         "خنثی": 0.5
#     },
#     "overall_accuracy": 0.8333
# }