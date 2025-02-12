import pandas as pd
import json

class DataFormatConsistency:
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Class to evaluate the format consistency of data records based on the first row's data types.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        """
        self.df = df
        self.invalid_rows = pd.DataFrame()
        self.compatible_items_count = 0
        self.incompatible_items_count = 0
        self.compatibility_ratio = 0.0
    
    def check_format_compatibility(self) -> None:
        """
        Check whether each row in the DataFrame is compatible with the first row's format.
        This checks the data types of each column in every row against the first row.
        """
        # Get the data types of the first row
        first_row = self.df.iloc[0]
        
        # Initialize counts for compatible and incompatible items
        compatible_items = 0
        incompatible_items = 0
        
        # Check format compatibility for each row
        for _, row in self.df.iterrows():
            compatible = True
            for col in self.df.columns:
                # Check if the type of current row's column matches the first row's column type
                if not isinstance(row[col], type(first_row[col])):
                    compatible = False
                    break
            if compatible:
                compatible_items += 1
            else:
                incompatible_items += 1
                self.invalid_rows = pd.concat([self.invalid_rows, pd.DataFrame([row])], ignore_index=True)
        
        self.compatible_items_count = compatible_items
        self.incompatible_items_count = incompatible_items
        
        # Calculate the ratio (Total compatible items / Total items in the dataset)
        if len(self.df) > 0:
            self.compatibility_ratio = compatible_items / len(self.df)
    
    def get_format_compatibility_report(self) -> str:
        """
        Generate a JSON-formatted report summarizing format compatibility and mismatched rows.
        
        Returns:
        - A JSON string containing the compatibility ratio and mismatched rows (with all columns).
        """
        # Convert the entire row of mismatched rows (all columns) to a list of dictionaries
        result = {
            "format_compatibility_ratio": self.compatibility_ratio,
            "mismatched_rows": self.invalid_rows.to_dict(orient='records')  # Include all columns
        }
        return json.dumps(result, ensure_ascii=False, indent=4)


#Example usage (Farsi Sentiment Dataset)
data = {
    "text": [
        "این یک محصول عالی است",  # Positive
        "کیفیت خیلی بد بود، ناراضی هستم",  # Negative
        "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
        "خرید این محصول را پیشنهاد نمی‌کنم",  # Negative
        12345  # Mismatched type (integer)
    ],
    "label": ["مثبت", 2, "خنثی", "منفی", 100],  # Mismatched type (integer)
    "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
}
df = pd.DataFrame(data)

# Data format consistency check
format_checker = DataFormatConsistency(df)
format_checker.check_format_compatibility()
print(format_checker.get_format_compatibility_report())

# Example Output:
    # {
    #     "format_compatibility_ratio": 0.6,
    #     "mismatched_rows": [
    #         {
    #             "text": "کیفیت خیلی بد بود، ناراضی هستم",
    #             "label": 2,
    #             "date": "2024-01-02"
    #         },
    #         {
    #             "text": 12345,
    #             "label": 100,
    #             "date": "2024-01-05"
    #         }
    #     ]
    # }