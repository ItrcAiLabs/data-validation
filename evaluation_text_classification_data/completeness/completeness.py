import json
import pandas as pd

# Assuming these classes are available from their corresponding modules
from .feature_completeness import FeatureCompleteness
from .record_completeness import RecordCompleteness
from .value_occurrence_completness import ValueOcurrenceCompletness  # Note the spelling as provided


def completeness(df: pd.DataFrame, label_column: str, expected_occurrences: dict) -> dict:
    """
    Evaluates the completeness of a DataFrame by performing:
      - Feature completeness check.
      - Record completeness check.
      - Label accuracy check.

    Parameters:
      df (pd.DataFrame): The input DataFrame.
      label_column (str): Name of the column containing labels.
      expected_occurrences (dict): A dictionary with expected occurrences for each label.

    Returns:
      dict: A dictionary containing reports for feature completeness, record completeness, and label accuracy.
    """
    # Feature completeness check
    completeness_checker = FeatureCompleteness(df)
    completeness_checker.evaluate_completeness()
    feature_completeness_report = completeness_checker.get_completeness_report()

    # Record completeness check
    record_checker = RecordCompleteness(df)
    record_checker.evaluate_record_completeness()
    record_completeness_report = record_checker.get_record_completeness_report()

    # Label accuracy check
    label_checker = ValueOcurrenceCompletness(df, label_column=label_column, expected_occurrences=expected_occurrences)
    label_checker.evaluate_label_accuracy()
    label_accuracy_report = label_checker.get_label_accuracy_report()

    # Combine all reports into one result dictionary
    completeness_result = {
        "feature_completeness_report": json.loads(feature_completeness_report),
        "record_completeness_report": json.loads(record_completeness_report),
        "label_accuracy_report": json.loads(label_accuracy_report)
    }

    # Print the combined result in a nicely formatted JSON structure
    return json.dumps(completeness_result, indent=4, ensure_ascii=False)


# Sample dataset with some missing values
# data = {
#     "text": [
#         "این یک محصول عالی است",             # Positive
#         "کیفیت خیلی بد بود، ناراضی هستم",     # Negative
#         "محصول متوسط بود، می‌توانست بهتر باشد",  # Neutral
#         None                                  # Missing value
#     ],
#     "label": ["مثبت", "خنثی", "خنثی", None],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
# }
# df = pd.DataFrame(data)

# # Define expected occurrences for each label
# expected_occurrences = {
#     "مثبت": 2,
#     "خنثی": 1
# }

# # Run the completeness checks (feature, record, and label accuracy)
# completeness_report = completeness(df, label_column="label", expected_occurrences=expected_occurrences)

# # Print the overall completeness report
# print("Overall Completeness Report:")
# print(completeness_report)

#output
    # {
    #     "feature_completeness_report": {
    #         "feature_completeness": {
    #             "text": 0.75,
    #             "label": 0.75,
    #             "date": 1.0
    #         },
    #         "missing_features": {
    #             "text": 1,
    #             "label": 1
    #         }
    #     },
    #     "record_completeness_report": {
    #         "record_completeness": 0.75,
    #         "records_with_missing_values": [
    #             {
    #                 "text": null,
    #                 "label": null,
    #                 "date": "2024-01-04"
    #             }
    #         ]
    #     },
    #     "label_accuracy_report": {
    #         "label_accuracy": {
    #             "خنثی": 0.5,
    #             "مثبت": 1
    #         },
    #         "overall_accuracy": 0.75
    #     }
    # }