import pandas as pd
import json
import re

class FeatureCurrentess:
    def __init__(self, df: pd.DataFrame, text_column: str, context: str):
        """
        Initializes the KeywordCurrentness class to evaluate the presence of keywords in text using regex for precise matching.
        
        :param df: DataFrame containing the text data.
        :param context: Context for which the relevant keywords will be loaded from the JSON file.
        """
        self.df = df
        self.text_column = text_column
        self.context = context
        
        # Load keyword data from JSON file based on the specified context
        with open("./currentness/data.json", "r") as file:
            self.keyword_data = json.load(file)[self.context]
        
        self.currentness_ratio = 0
        self.kept_records = pd.DataFrame()

        # Precompile a regex pattern to search for any of the keywords using word boundaries for accuracy
        escaped_keywords = [re.escape(keyword) for keyword in self.keyword_data]
        self.pattern = re.compile(r'\b(?:' + '|'.join(escaped_keywords) + r')\b', flags=re.IGNORECASE | re.UNICODE)

    def evaluate_currentness(self):
        """  
        Evaluates currentness based on the presence of keywords in the 'text' column using the precompiled regex.
        """
        # Ensure the DataFrame contains a 'text' column
        if 'text' not in self.df.columns:
            raise ValueError("DataFrame must contain a 'text' column")
        
        # Check for the presence of any keyword in each text entry
        has_keyword = self.df[self.text_column].apply(lambda text: bool(self.pattern.search(text)))
        
        # Filter records that contain at least one keyword
        self.kept_records = self.df[has_keyword]
        total_rows = len(self.df)
        self.currentness_ratio = len(self.kept_records) / total_rows if total_rows > 0 else 0

    def get_feature_currentness_report(self) -> dict:
        """
        Generates a report containing the currentness ratio and the filtered records.
        
        :return: A dictionary with the currentness ratio and the list of filtered records.
        """
        result =  {
            "currentness_ratio": self.currentness_ratio,
            "kept_records": self.kept_records.to_dict(orient='records')
        }
        return json.dumps(result, ensure_ascii=False, indent=4)

# Example usage
# data = {
#     "text": [
#         "این محصول فاز بدی دارد",  # Contains a sentiment keyword
#         "او یک ساندیس‌ خور حرفه‌ای است",  # Contains a political keyword
#         "این یک متن خنثی است",  # No keywords present
#         "مسائل اصلاحات همیشه چالش‌برانگیز است"  # Contains a political keyword
#     ],
#     "timestamp": ["2024-01-01", "2023-07-15", "2022-06-01", "2023-11-10"]
# }
# df = pd.DataFrame(data)

# # Analyze currentness for the "Political" context
# analyzer = FeatureCurrentess(df, "text" , "Political")
# analyzer.evaluate_currentness()
# report = analyzer.get_feature_currentness_report()

# print(report)


    # output
        # {
        # "currentness_ratio": 0.5,
        # "kept_records": [
        #     {
        #         "text": "او یک ساندیس‌ خور حرفه‌ای است",
        #         "timestamp": "2023-07-15"
        #     },
        #     {
        #         "text": "مسائل اصلاحات همیشه چالش‌برانگیز است",
        #         "timestamp": "2023-11-10"
        #     }
        # ]
        # }
