import pandas as pd
import json

from currentness.currentness import currentness
from completeness.completeness import completeness
from accuracy.accuracy import accuracy
from consistency.consistency import consistency


def classification(df, config):
    """
    Perform a comprehensive data quality classification on the input DataFrame.

    This function executes four quality checks on the data:
      1. Currentness Check: Assesses the recency of data based on a timestamp.
      2. Completeness Check: Evaluates missing values and verifies expected label occurrences.
      3. Consistency Check: Checks for format compatibility, duplicate records, and semantic conflicts.
      4. Accuracy Check: Examines semantic, syntactic, and model-based accuracy along with risk assessment.

    Parameters:
    -----------
    df : pd.DataFrame
        The input DataFrame containing the dataset.

    config : dict
        A configuration dictionary with optional keys for each quality check:
        
        - "currentness": A dictionary of parameters for the currentness function, e.g.:
              {
                  "text_column": "text",
                  "context": "Political",
                  "timestamp_col": "timestamp",
                  "threshold_days": 600
              }
              
        - "completeness": A dictionary of parameters for the completeness function, e.g.:
              {
                  "label_column": "label",
                  "expected_occurrences": {"مثبت": 2, "خنثی": 1}
              }
              
        - "consistency": A dictionary of parameters for the consistency function, e.g.:
              {
                  "text_column": "text",
                  "label_column": "label",
                  "date_column": "date",
                  "similarity_threshold": 0.95
              }
              
        - "accuracy": A dictionary of parameters for the accuracy function (if applicable).

    Returns:
    --------
    dict
        A combined report containing the results from the quality checks. The keys in the returned dictionary 
        may include:
            - "currentness_report"
            - "completeness_report"
            - "consistency_report"
            - "accuracy_report"
    """
    # Initialize a dictionary to hold the overall report
    combined_report = {}

    # Execute the currentness check if parameters are provided
    if "currentness" in config and config["currentness"]:
        combined_report["currentness_report"] = json.loads(currentness(df, **config["currentness"]))

    # Execute the completeness check if parameters are provided
    if "completeness" in config and config["completeness"]:
        combined_report["completeness_report"] = json.loads(completeness(df, **config["completeness"]))

    # Execute the consistency check if parameters are provided
    if "consistency" in config and config["consistency"]:
        combined_report["consistency_report"] = json.loads(consistency(df, **config["consistency"]))

    # Execute the accuracy check if parameters are provided
    if "accuracy" in config and config["accuracy"]:
        combined_report["accuracy_report"] = json.loads(accuracy(df, **config["accuracy"]))

    # Return the aggregated report containing all checks
    return json.dumps(combined_report, indent=4, ensure_ascii=False)





# Sample DataFrame for demonstration purposes
# data = {
#     "text": [
#         "این محصول فاز بدی دارد",              # Contains a sentiment keyword (for currentness check)
#         "او یک ساندیس‌ خور حرفه‌ای استhttps://divar.ir/s/tehran?q=Xiaomi%2012",        # Contains a political keyword
#         "این یک متن خنثی است",                  # No keywords present
#         "مسائل اصلاحات همیشه چالش‌برانگیز است"   # Contains a political keyword
#     ],
#     "timestamp": ["2024-01-01", "2023-07-15", "2022-06-01", "2023-11-10"],
#     "label": ["مثبت", "منفی", "خنثی", "منفی"],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
# }
# df = pd.DataFrame(data)

# mapping_label = {
#     "furious": "منفی",
#     "angry": "عصبانی",
#     "neutral": "خنثی",
#     "happy": "خوشحال",
#     "delighted": "مثبت"
# }

# required_columns = ["id", "text", "label", "date"]
# required_size = 3  # Adjusted to match the sample data size

# # Define a configuration dictionary for all quality checks
# config = {
#     "currentness": {
#         "text_column": "text",
#         "context": "Political",          # Context keyword for currentness check
#         "timestamp_col": "timestamp",
#         "threshold_days": 600
#     },
#     "completeness": {
#         "label_column": "label",
#         "expected_occurrences": {"مثبت": 2, "خنثی": 1}
#     },
#     "consistency": {
#         "text_column": "text",
#         "label_column": "label",
#         "date_column": "date",
#         "similarity_threshold": 0.95
#     },
#     "accuracy": {
#         "required_columns": required_columns,  # List of mandatory columns
#         "required_size": required_size,         # Minimum dataset size
#         "text_column": "text",
#         "date_column": "date",
#         "min_length": 5,                       # Minimum text length
#         "max_length": 50,                       # Maximum text length
#         "start_date": "2024-01-01",             # Earliest valid date
#         "end_date": "2024-12-31",               # Latest valid date
#         "sequence_of_operations": [
#             "remove_links",
#             "remove_phone_numbers",
#             "remove_extra_spaces"
#         ],                                      # Text cleaning steps
#         "mapping_label": mapping_label,         # Label mapping dictionary
#         "semantic_task": "sentiment",           # NLP task type
#         "semantic_model_name": "deepsentipers"  # Validation model
#     }
# }

# # Execute the classification function using the sample DataFrame and configuration
# report = classification(df, config)

# # Print the combined quality report
# print(report)
# # print(**config["currentness"])

# output

    # {
    #     "currentness_report": {
    #         "feature_currentness": {
    #             "currentness_ratio": 0.5,
    #             "kept_records": [
    #                 {
    #                     "text": "او یک ساندیس‌ خور حرفه‌ای استhttps://divar.ir/s/tehran?q=Xiaomi%2012",
    #                     "timestamp": "2023-07-15",
    #                     "label": "منفی",
    #                     "date": "2024-01-02"
    #                 },
    #                 {
    #                     "text": "مسائل اصلاحات همیشه چالش‌برانگیز است",
    #                     "timestamp": "2023-11-10",
    #                     "label": "منفی",
    #                     "date": "2024-01-04"
    #                 }
    #             ]
    #         },
    #         "record_currentness": {
    #             "record_currentness": 0.75,
    #             "outdated_records": [
    #                 {
    #                     "text": "این یک متن خنثی است",
    #                     "timestamp": "2022-06-01 00:00:00",
    #                     "label": "خنثی",
    #                     "date": "2024-01-03",
    #                     "age": 989
    #                 }
    #             ]
    #         }
    #     },
    #     "completeness_report": {
    #         "feature_completeness_report": {
    #             "feature_completeness": {
    #                 "text": 1.0,
    #                 "timestamp": 1.0,
    #                 "label": 1.0,
    #                 "date": 1.0,
    #                 "age": 1.0
    #             },
    #             "missing_features": {}
    #         },
    #         "record_completeness_report": {
    #             "record_completeness": 1.0,
    #             "records_with_missing_values": []
    #         },
    #         "label_accuracy_report": {
    #             "label_accuracy": {
    #                 "مثبت": 1,
    #                 "خنثی": 1
    #             },
    #             "overall_accuracy": 1.0
    #         }
    #     },
    #     "consistency_report": {
    #         "format_compatibility_report": {
    #             "format_compatibility_ratio": 0.0,
    #             "mismatched_rows": [
    #                 {
    #                     "text": "این محصول فاز بدی دارد",
    #                     "timestamp": "2024-01-01 00:00:00",
    #                     "label": "مثبت",
    #                     "date": "2024-01-01",
    #                     "age": 410
    #                 },
    #                 {
    #                     "text": "او یک ساندیس‌ خور حرفه‌ای استhttps://divar.ir/s/tehran?q=Xiaomi%2012",
    #                     "timestamp": "2023-07-15 00:00:00",
    #                     "label": "منفی",
    #                     "date": "2024-01-02",
    #                     "age": 580
    #                 },
    #                 {
    #                     "text": "این یک متن خنثی است",
    #                     "timestamp": "2022-06-01 00:00:00",
    #                     "label": "خنثی",
    #                     "date": "2024-01-03",
    #                     "age": 989
    #                 },
    #                 {
    #                     "text": "مسائل اصلاحات همیشه چالش‌برانگیز است",
    #                     "timestamp": "2023-11-10 00:00:00",
    #                     "label": "منفی",
    #                     "date": "2024-01-04",
    #                     "age": 462
    #                 }
    #             ]
    #         },
    #         "record_consistency_report": {
    #             "duplicate_ratio": 0.0,
    #             "total_records": 4,
    #             "duplicate_count": 0,
    #             "duplicates": []
    #         },
    #         "distribution_report": {
    #             "label_distribution": {
    #                 "منفی": 2,
    #                 "مثبت": 1,
    #                 "خنثی": 1
    #             }
    #         },
    #         "semantic_consistency_report": {
    #             "semantic_consistency_ratio": 1.0,
    #             "mismatched_rows": []
    #         }
    #     },
    #     "accuracy_report": {
    #         "semantic_accuracy": {
    #             "accuracy": 0.0,
    #             "conflicts": [
    #                 {
    #                     "index": 0,
    #                     "text": "این محصول فاز بدی دارد",
    #                     "actual_label": "مثبت",
    #                     "predicted_label": "عصبانی"
    #                 },
    #                 {
    #                     "index": 1,
    #                     "text": "او یک ساندیس‌ خور حرفه‌ای استhttps://divar.ir/s/tehran?q=Xiaomi%2012",
    #                     "actual_label": "منفی",
    #                     "predicted_label": "خوشحال"
    #                 },
    #                 {
    #                     "index": 2,
    #                     "text": "این یک متن خنثی است",
    #                     "actual_label": "خنثی",
    #                     "predicted_label": "خوشحال"
    #                 },
    #                 {
    #                     "index": 3,
    #                     "text": "مسائل اصلاحات همیشه چالش‌برانگیز است",
    #                     "actual_label": "منفی",
    #                     "predicted_label": "عصبانی"
    #                 }
    #             ]
    #         },
    #         "syntactic_accuracy": {
    #             "accuracy": 0.25,
    #             "problematic_data": {
    #                 "remove_links": [
    #                     "او یک ساندیس‌ خور حرفه‌ای استhttps://divar.ir/s/tehran?q=Xiaomi%2012"
    #                 ]
    #             }
    #         },
    #         "model_accuracy": {
    #             "accuracy_scores": {
    #                 "column_presence": 0.75,
    #                 "size_requirement": 1.0
    #             },
    #             "overall_accuracy": 0.875,
    #             "missing_columns": [
    #                 "id"
    #             ]
    #         },
    #         "risk_assessment": {
    #             "risk_scores": {
    #                 "text_length": 0.75,
    #                 "date_validity": 1.0
    #             },
    #             "average_risk": 0.88,
    #             "outlier_texts": [
    #                 "او یک ساندیس‌ خور حرفه‌ای استhttps://divar.ir/s/tehran?q=Xiaomi%2012"
    #             ],
    #             "outlier_dates": [
    #                 "2024-01-02"
    #             ]
    #         }
    #     }
    # }