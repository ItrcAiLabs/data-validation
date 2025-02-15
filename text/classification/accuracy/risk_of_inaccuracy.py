"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""
import json
import pandas as pd
from datetime import datetime

class RiskOfInaccuracy:
    def __init__(self, df: pd.DataFrame, text_column: str = 'text', date_column: str = 'date',
                 min_length: int = 5, max_length: int = 500, start_date: str = '1900-01-01',
                 end_date: str = '2100-12-31'):
        """
        Class for calculating the risk of inaccuracy in data by identifying texts with invalid lengths and checking date validity.
        
        Parameters:
        - df: Pandas DataFrame containing the data.
        - text_column: Name of the column containing the text.
        - date_column: Name of the column containing the date.
        - min_length: Minimum allowed text length.
        - max_length: Maximum allowed text length.
        - start_date: Earliest allowed date.
        - end_date: Latest allowed date.
        """
        self.df = df.copy()
        self.text_column = text_column
        self.date_column = date_column
        self.min_length = min_length
        self.max_length = max_length
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        self.risk_scores = {}
        # Store outlier results for text and date separately
        self.text_length_outliers = pd.DataFrame()
        self.date_outliers = pd.DataFrame()
    
    def check_text_length(self) -> float:
        """
        Identify texts that are out of the allowed length range (either too short or too long).
        
        Returns:
        - A risk score based on the proportion of texts that are outliers.
        """
        self.df['text_length'] = self.df[self.text_column].apply(len)
        self.text_length_outliers = self.df[(self.df['text_length'] < self.min_length) | 
                                            (self.df['text_length'] > self.max_length)]
        risk = 1 - (len(self.text_length_outliers) / len(self.df) if len(self.df) > 0 else 0)
        self.risk_scores['text_length'] = round(risk, 2)
        return risk
    
    def check_date_validity(self) -> float:
        """
        Check the validity of dates for texts that have a sufficient length (>= min_length).
        
        Returns:
        - A risk score based on the proportion of invalid dates.
        """
        # Only check rows with sufficient text length
        valid_texts = self.df[self.df['text_length'] >= self.min_length]
        invalid_indices = []
        for idx, row in valid_texts.iterrows():
            date_str = row[self.date_column]
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if not (self.start_date <= date_obj <= self.end_date):
                    invalid_indices.append(idx)
            except ValueError:
                invalid_indices.append(idx)
        
        self.date_outliers = valid_texts.loc[invalid_indices]
        risk = 1 - (len(self.date_outliers) / len(valid_texts) if len(valid_texts) > 0 else 0)
        self.risk_scores['date_validity'] = round(risk, 2)
        return risk
    
    def calculate_average_risk(self) -> float:
        """
        Calculate the average risk score.
        """
        return round(sum(self.risk_scores.values()) / len(self.risk_scores) if self.risk_scores else 0, 2)
    
    def get_risk_assessment(self) -> str:
        """
        Generate a final JSON report including risk scores, average risk, and outlier data.
        Note: In the outlier_dates list, dates corresponding to texts that are too short (less than min_length) are excluded.
        
        Returns:
        - A JSON-formatted string summarizing the risk assessment.
        """
        # All texts that are outliers due to invalid length
        all_outlier_texts = self.text_length_outliers[self.text_column].tolist()
        
        # From the outlier texts, consider only those with sufficient length (i.e., texts that are too long)
        text_length_date_outliers = self.text_length_outliers[self.text_length_outliers['text_length'] >= self.min_length][self.date_column].tolist()
        # Also include dates from the invalid date check
        date_validity_outliers = self.date_outliers[self.date_column].tolist()
        
        # Combine dates (without duplicates) and maintain the original order from the DataFrame
        combined_dates = list(set(text_length_date_outliers + date_validity_outliers))
        outlier_dates = [date for date in self.df[self.date_column].tolist() if date in combined_dates]
        
        result = {
            "risk_scores": self.risk_scores,
            "average_risk": self.calculate_average_risk(),
            "outlier_texts": all_outlier_texts,
            "outlier_dates": outlier_dates
        }
        
        return json.dumps(result, ensure_ascii=False, indent=4)

# ----------------- Example Usage -----------------

# data = {
#     "text": [
#         "این محصول فوق‌العاده بود!",  # Valid length
#         "محصول",  # Too short (outlier due to short length)
#         "من از این خرید کاملاً راضی هستم و به همه پیشنهاد می‌کنم.",  # Too long (outlier due to excessive length)
#         "محصول افتضاح بود و اصلاً توصیه نمی‌کنم. کیفیت بسیار پایین و ارسال خیلی دیر انجام شد. برخورد پشتیبانی هم خوب نبود.",  # Too long (outlier due to excessive length)
#         "متوسط بود"  # Valid length
#     ],
#     "label": ["مثبت", "منفی", "مثبت", "منفی", "خنثی"],
#     "date": ["2024-02-01", "2024-02-02", "2024-02-03", "2024-02-04", "2024-02-05"]
# }

# df = pd.DataFrame(data)

# Set parameters: minimum length 7, maximum length 50, and date range in 2024
# risk_checker = RiskOfInaccuracy(df, text_column="text", date_column="date", 
#                                   min_length=7, max_length=50, 
#                                   start_date="2024-01-01", end_date="2024-12-31")

# risk_checker.check_text_length()
# risk_checker.check_date_validity()
# report = risk_checker.get_risk_assessment()
# print(report)


# output
    # {
    #     "risk_scores": {
    #         "text_length": 0.4,
    #         "date_validity": 1.0
    #     },
    #     "average_risk": 0.7,
    #     "outlier_texts": [
    #         "محصول",
    #         "من از این خرید کاملاً راضی هستم و به همه پیشنهاد می‌کنم.",
    #         "محصول افتضاح بود و اصلاً توصیه نمی‌کنم. کیفیت بسیار پایین و ارسال خیلی دیر انجام شد. برخورد پشتیبانی هم خوب نبود."
    #     ],
    #     "outlier_dates": [
    #         "2024-02-03",
    #         "2024-02-04"
    #     ]
    # }