import json
import pandas as pd
from .data_format_consistency import DataFormatConsistency
from .data_record_consistency import DataRecordConsistency
from .data_value_distribution import DataValueDistribution
from .semantic_consistency import SemanticConsistency


def consistency(df: pd.DataFrame,
                text_column: str,
                label_column: str,
                date_column: str,
                similarity_threshold: float = 0.9) -> dict:
    """
    Runs a series of consistency checks on the given DataFrame:
      - Data Format Consistency
      - Data Record Consistency
      - Data Value Distribution
      - Data Semantic Consistency

    Parameters:
      df (pd.DataFrame): Input DataFrame.
      text_column (str): Column name for text data.
      label_column (str): Column name for label data.
      date_column (str): Column name for date information.
      similarity_threshold (float): Threshold for similarity in consistency checks.

    Returns:
      dict: A dictionary containing reports from all consistency checks.
    """
    # Data Format Consistency Check
    format_checker = DataFormatConsistency(df)
    format_checker.check_format_compatibility()
    format_compatibility_report = format_checker.get_format_compatibility_report()

    # Data Record Consistency Check
    record_checker = DataRecordConsistency(df, similarity_threshold=similarity_threshold)
    record_checker.evaluate_consistency()
    record_consistency_report = record_checker.get_consistency_report()

    # Data Value Distribution Check
    distribution_checker = DataValueDistribution(df)
    distribution_checker.analyze_distribution()
    distribution_report = distribution_checker.get_distribution_report()

    # Data Semantic Consistency Check
    semantic_checker = SemanticConsistency(
        df,
        text_column=text_column,
        label_column=label_column,
        date_column=date_column,
        similarity_threshold=similarity_threshold
    )
    semantic_checker.check_semantic_consistency()
    semantic_consistency_report = semantic_checker.get_semantic_consistency_report()

    # Combine all reports into one dictionary
    consistency_result = {
        "format_compatibility_report": json.loads(format_compatibility_report),
        "record_consistency_report": json.loads(record_consistency_report),
        "distribution_report": json.loads(distribution_report),
        "semantic_consistency_report": json.loads(semantic_consistency_report)
    }

    # Print the result in a nicely formatted JSON structure
    return json.dumps(consistency_result, indent=4, ensure_ascii=False)


# ---------------------- Example Usage ----------------------

# Example Farsi Sentiment Dataset with some mismatches
# data = {
#     "text": [
#         "این یک محصول عالی است",             # Expected type: string (Positive sentiment)
#         "کیفیت خیلی بد بود، ناراضی هستم",     # Expected type: string (Negative sentiment)
#         "محصول متوسط بود، می‌توانست بهتر باشد", # Expected type: string (Neutral sentiment)
#         "خرید این محصول را پیشنهاد نمی‌کنم",   # Expected type: string (Negative sentiment)
#         "1234",                                 # Mismatched type (integer)
#         "این یک محصول تقریبا عالی است",
#     ],
#     "label": ["مثبت", 2, "خنثی", "منفی", 100, "خنثی"],  # Mismatched types for labels (integer in some rows)
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05", "2024-11-04"]
# }
# df = pd.DataFrame(data)

# # Running the overall consistency checks with a custom similarity threshold (if needed)
# consistency_results = consistency(df,
#                                     text_column="text",
#                                     label_column="label",
#                                     date_column="date",
#                                     similarity_threshold=0.95)

    # {
    #     "format_compatibility_report": {
    #         "format_compatibility_ratio": 0.6666666666666666,
    #         "mismatched_rows": [
    #             {
    #                 "text": "کیفیت خیلی بد بود، ناراضی هستم",
    #                 "label": 2,
    #                 "date": "2024-01-02"
    #             },
    #             {
    #                 "text": "1234",
    #                 "label": 100,
    #                 "date": "2024-01-05"
    #             }
    #         ]
    #     },
    #     "record_consistency_report": {
    #         "duplicate_ratio": 0.33,
    #         "total_records": 6,
    #         "duplicate_count": 2,
    #         "duplicates": [
    #             {
    #                 "text": "این یک محصول عالی است",
    #                 "label": "مثبت",
    #                 "date": "2024-01-01"
    #             },
    #             {
    #                 "text": "این یک محصول تقریبا عالی است",
    #                 "label": "خنثی",
    #                 "date": "2024-11-04"
    #             }
    #         ]
    #     },
    #     "distribution_report": {
    #         "label_distribution": {
    #             "خنثی": 2,
    #             "مثبت": 1,
    #             "2": 1,
    #             "منفی": 1,
    #             "100": 1
    #         }
    #     },
    #     "semantic_consistency_report": {
    #         "semantic_consistency_ratio": 0.67,
    #         "mismatched_rows": [
    #             {
    #                 "text": "این یک محصول عالی است",
    #                 "label": "مثبت",
    #                 "date": "2024-01-01",
    #                 "conflicts_with": [
    #                     {
    #                         "label": "خنثی",
    #                         "date": "2024-11-04",
    #                         "similarity_score": 0.9799855947494507
    #                     }
    #                 ]
    #             },
    #             {
    #                 "text": "این یک محصول تقریبا عالی است",
    #                 "label": "خنثی",
    #                 "date": "2024-11-04",
    #                 "conflicts_with": [
    #                     {
    #                         "label": "مثبت",
    #                         "date": "2024-01-01",
    #                         "similarity_score": 0.9799855947494507
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }
    # (myenv) ➜  consistency git:(main) ✗ python3 consistency.py
    # {
    #     "format_compatibility_report": {
    #         "format_compatibility_ratio": 0.6666666666666666,
    #         "mismatched_rows": [
    #             {
    #                 "text": "کیفیت خیلی بد بود، ناراضی هستم",
    #                 "label": 2,
    #                 "date": "2024-01-02"
    #             },
    #             {
    #                 "text": "1234",
    #                 "label": 100,
    #                 "date": "2024-01-05"
    #             }
    #         ]
    #     },
    #     "record_consistency_report": {
    #         "duplicate_ratio": 0.33,
    #         "total_records": 6,
    #         "duplicate_count": 2,
    #         "duplicates": [
    #             {
    #                 "text": "این یک محصول عالی است",
    #                 "label": "مثبت",
    #                 "date": "2024-01-01"
    #             },
    #             {
    #                 "text": "این یک محصول تقریبا عالی است",
    #                 "label": "خنثی",
    #                 "date": "2024-11-04"
    #             }
    #         ]
    #     },
    #     "distribution_report": {
    #         "label_distribution": {
    #             "خنثی": 2,
    #             "مثبت": 1,
    #             "2": 1,
    #             "منفی": 1,
    #             "100": 1
    #         }
    #     },
    #     "semantic_consistency_report": {
    #         "semantic_consistency_ratio": 0.67,
    #         "mismatched_rows": [
    #             {
    #                 "text": "این یک محصول عالی است",
    #                 "label": "مثبت",
    #                 "date": "2024-01-01",
    #                 "conflicts_with": [
    #                     {
    #                         "text": "این یک محصول تقریبا عالی است",
    #                         "label": "خنثی",
    #                         "date": "2024-11-04",
    #                         "similarity_score": 0.9799855947494507
    #                     }
    #                 ]
    #             },
    #             {
    #                 "text": "این یک محصول تقریبا عالی است",
    #                 "label": "خنثی",
    #                 "date": "2024-11-04",
    #                 "conflicts_with": [
    #                     {
    #                         "text": "این یک محصول عالی است",
    #                         "label": "مثبت",
    #                         "date": "2024-01-01",
    #                         "similarity_score": 0.9799855947494507
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    # }