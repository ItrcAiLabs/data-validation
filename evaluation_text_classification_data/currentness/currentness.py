import pandas as pd
import json

from .feature_currentess import FeatureCurrentess
from .record_currentness import RecordCurrentness


def currentness(df: pd.DataFrame, text_column: str, context: str, timestamp_col='timestamp', threshold_days=180) -> dict:
    """
    Evaluate currentness using both feature and record analyses.
    
    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        text_column (str): Column name containing text data.
        context (str): Context used for feature currentness analysis (e.g., "Political").
        timestamp_col (str): Column name for timestamp data.
        threshold_days (int): Age threshold in days for record currentness.
    
    Returns:
        dict: Combined report with both feature and record currentness.
    """
    currentness_report = {}

    # Feature currentness analysis (e.g., filtering text based on the given context)
    analyzer = FeatureCurrentess(df, text_column=text_column, context=context)
    analyzer.evaluate_currentness()
    feature_currentness_report = analyzer.get_feature_currentness_report()

    # Record currentness analysis (e.g., checking if records are outdated based on their timestamp)
    currentness_checker = RecordCurrentness(df, threshold_days=threshold_days)
    currentness_checker.evaluate_currentness()
    record_currentness_report = currentness_checker.get_currentness_report()

    # Combine both reports into one dictionary
    currentness_report['feature_currentness'] = json.loads(feature_currentness_report)
    currentness_report['record_currentness'] = json.loads(record_currentness_report)

    return json.dumps(currentness_report, indent=4, ensure_ascii=False)



# Assuming that currentness, FeatureCurrentess, and RecordCurrentness have been defined/imported properly
# from feature_currentess import FeatureCurrentess
# from record_currentness import RecordCurrentness

# Sample DataFrame with text and timestamp data
# data = {
#     "text": [
#         "این محصول فاز بدی دارد",              # Contains a sentiment keyword
#         "او یک ساندیس‌ خور حرفه‌ای است",        # Contains a political keyword
#         "این یک متن خنثی است",                  # No keywords present
#         "مسائل اصلاحات همیشه چالش‌برانگیز است"   # Contains a political keyword
#     ],
#     "timestamp": ["2024-01-01", "2023-07-15", "2022-06-01", "2023-11-10"]
# }
# df = pd.DataFrame(data)

# # Use the currentness function to obtain a combined report
# ccurrentness_report = currentness(df, text_column="text", context="Political", timestamp_col="timestamp", threshold_days=600)

# print(ccurrentness_report)


#out put
# {
#     "feature_currentness": {
#         "currentness_ratio": 0.5,
#         "kept_records": [
#             {
#                 "text": "او یک ساندیس‌ خور حرفه‌ای است",
#                 "timestamp": "2023-07-15"
#             },
#             {
#                 "text": "مسائل اصلاحات همیشه چالش‌برانگیز است",
#                 "timestamp": "2023-11-10"
#             }
#         ]
#     },
#     "record_currentness": {
#         "record_currentness": 0.75,
#         "outdated_records": [
#             {
#                 "text": "این یک متن خنثی است",
#                 "timestamp": "2022-06-01 00:00:00",
#                 "age": 988
#             }
#         ]
#     }
# }
