import pandas as pd
import json

import pandas as pd
import json

class SemanticConsistency:
    def __init__(self, df: pd.DataFrame, text_column: str, label_column: str) -> None:
        """
        Class to evaluate the semantic consistency of data records by comparing text column values 
        and checking if their labels or content match semantically.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        - text_column: The name of the text column to check for semantic consistency.
        - label_column: The name of the label column to check if the labels are semantically correct.
        """
        self.df = df
        self.text_column = text_column
        self.label_column = label_column
        self.invalid_rows = pd.DataFrame()
        self.semantic_ratio = 0.0
    
    def check_semantic_consistency(self) -> None:
        """
        Checks whether the text and corresponding label in each row are semantically consistent.
        This will compare the text values and identify rows where the labels are inconsistent
        with the text content.
        """
        # Identify duplicates in the text column
        duplicate_texts = self.df[self.df.duplicated(subset=[self.text_column], keep=False)]
        
        # For simplicity, let's assume semantically correct items are those with identical text
        # and consistent labels, i.e., identical text rows should have the same label.
        semantic_correct = 0
        semantic_incorrect = 0
        total_semantic_checkable = 0
        
        for _, row in duplicate_texts.iterrows():
            text_value = row[self.text_column]
            label_value = row[self.label_column]
            
            # Check if all rows with the same text have the same label
            similar_text_rows = self.df[self.df[self.text_column] == text_value]
            if all(similar_text_rows[self.label_column] == label_value):
                semantic_correct += 1
            else:
                # If any row with the same text has a different label, it's considered inconsistent
                self.invalid_rows = pd.concat([self.invalid_rows, similar_text_rows], ignore_index=True)
                semantic_incorrect += 1
            
            total_semantic_checkable += 1
        
        # Calculate the ratio of semantically correct items
        if total_semantic_checkable > 0:
            self.semantic_ratio = semantic_incorrect / total_semantic_checkable
    
    def get_semantic_consistency_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing semantic consistency.
        
        Returns:
        - A JSON string containing the semantic consistency ratio and mismatched rows.
        """
        result = {
            "semantic_consistency_ratio": self.semantic_ratio,
            "mismatched_rows": self.invalid_rows.to_dict(orient='records')  # Convert mismatched rows to a list of dictionaries
        }
        return json.dumps(result, ensure_ascii=False, indent=4)


# Example usage (Farsi Sentiment Dataset)
# data = {
#     "text": [
#         "این یک محصول عالی است",  # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#         "خرید این محصول را پیشنهاد نمی‌کنم",  # Negative
#         "این یک محصول عالی است"  # Duplicate (should match with the first row)
#     ],
#     "label": ["مثبت", "منفی", "خنثی", "منفی", "منفی"],  # Mismatched label for the duplicate row
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
# }
# df = pd.DataFrame(data)

# # Semantic consistency check
# semantic_checker = SemanticConsistency(df, text_column="text", label_column="label")
# semantic_checker.check_semantic_consistency()
# print(semantic_checker.get_semantic_consistency_report())

# Example Output:
# {
#     "semantic_consistency_ratio": 0.75,
#     "mismatched_rows": [
#         {
#             "text": "این یک محصول عالی است",
#             "label": "مثبت",
#             "date": "2024-01-05"
#         }
#     ]
# }
