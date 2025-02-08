"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import json
import pandas as pd
from datetime import datetime

class RiskOfInaccuracy:
    def __init__(self, df: pd.DataFrame, text_column: str = 'text', date_column: str = 'date', min_length: int = 5, max_length: int = 500, start_date: str = '1900-01-01', end_date: str = '2100-12-31'):
        """
        Class to calculate the risk of dataset inaccuracy by identifying outlier texts based on length and invalid dates.
        
        Parameters:
        - df: Pandas DataFrame containing the dataset.
        - text_column: Column name representing the text data.
        - date_column: Column name representing the date data.
        - min_length: Minimum allowed text length.
        - max_length: Maximum allowed text length.
        - start_date: Minimum allowed date.
        - end_date: Maximum allowed date.
        """
        self.df = df
        self.text_column = text_column
        self.date_column = date_column
        self.min_length = min_length
        self.max_length = max_length
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        self.outliers = pd.DataFrame()
        self.risk_scores = {}
    
    def check_text_length(self) -> float:
        """
        Identify texts that are outliers based on length constraints.
        
        Returns:
        - Risk score based on the proportion of outlier texts.
        """
        self.df['text_length'] = self.df[self.text_column].apply(len)
        self.outliers = self.df[(self.df['text_length'] < self.min_length) | (self.df['text_length'] > self.max_length)]
        risk = len(self.outliers) / len(self.df) if len(self.df) > 0 else 0
        self.risk_scores['text_length'] = risk
        return risk
    
    def check_date_validity(self) -> float:
        """
        Identify invalid dates that are either out of the valid range or contain incorrect values.
        
        Returns:
        - Risk score based on the proportion of invalid dates.
        """
        invalid_dates = []
        for idx, date_str in enumerate(self.df[self.date_column]):
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if not (self.start_date <= date_obj <= self.end_date):
                    invalid_dates.append(idx)
            except ValueError:
                invalid_dates.append(idx)
        
        self.outliers = pd.concat([self.outliers, self.df.iloc[invalid_dates]])
        risk = len(invalid_dates) / len(self.df) if len(self.df) > 0 else 0
        self.risk_scores['date_validity'] = risk
        return risk
    
    def calculate_average_risk(self) -> float:
        """
        Calculate the average risk score by averaging the individual risk scores.
        
        Returns:
        - A float value representing the mean risk of all checks performed.
        """
        return sum(self.risk_scores.values()) / len(self.risk_scores) if self.risk_scores else 0
    
    def get_risk_assessment(self) -> str:
        """
        Generate a JSON-formatted report containing risk scores, average risk, and outlier data.
        
        Returns:
        - A JSON string summarizing the risk assessment, with outliers and invalid dates.
        """
        # Get the outlier texts and invalid dates separately
        outlier_texts = self.outliers[self.text_column].tolist() if not self.outliers.empty else []
        invalid_dates = self.outliers[self.date_column].tolist() if not self.outliers.empty else []
        
        # Prepare the result with additional outlier information
        result = {
            "risk_scores": self.risk_scores,
            "average_risk": self.calculate_average_risk(),
            "outlier_texts": outlier_texts,
            "outlier_dates": invalid_dates
        }
        
        return json.dumps(result, ensure_ascii=False, indent=4)



# Example usage (Farsi Sentiment Dataset)

# data = {
#     "text": [
#         "این محصول فوق‌العاده بود!",  # Valid length
#         "خیلی بد",  # Too short (outlier)
#         "من از این خرید کاملاً راضی هستم و به همه پیشنهاد می‌کنم.",  # Valid length
#         "محصول افتضاح بود و اصلاً توصیه نمی‌کنم. کیفیت بسیار پایین و ارسال خیلی دیر انجام شد. برخورد پشتیبانی هم خوب نبود.",  # Too long (outlier)
#         "متوسط بود"  # Valid length
#     ],
#     "label": ["مثبت", "منفی", "مثبت", "منفی", "خنثی"],
#     "date": ["2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04", "2024-02-05"]
# }


# df = pd.DataFrame(data)

# risk_checker = RiskOfInaccuracy(df, text_column="text", date_column="date", min_length=5, max_length=50, start_date="2024-01-01", end_date="2024-12-31")

# risk_checker.check_text_length()

# risk_checker.check_date_validity()
# report = risk_checker.get_risk_assessment()
# print(report)


# output

    # {
    #     "risk_scores": {
    #         "text_length": 0.4,
    #         "date_validity": 0.0
    #     },
    #     "average_risk": 0.2,
    #     "outlier_texts": [
    #         "من از این خرید کاملاً راضی هستم و به همه پیشنهاد می‌کنم.",
    #         "محصول افتضاح بود و اصلاً توصیه نمی‌کنم. کیفیت بسیار پایین و ارسال خیلی دیر انجام شد. برخورد پشتیبانی هم خوب نبود."
    #     ],
    #     "outlier_dates": [
    #         "2024-02-03",
    #         "2024-02-04"
    #     ]
    # }
