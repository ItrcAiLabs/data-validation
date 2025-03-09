import pandas as pd
import json
from .data_model_accuracy import DataModelAccuracy
from .risk_of_inaccuracy import RiskOfInaccuracy
from .syntactic_accuracy import SyntacticAccuracy
from .semantic_accuracy import SemanticACcuracy

def accuracy(df: pd.DataFrame, 
             required_columns: list, 
             required_size: int,
             text_column: str = 'text', 
             date_column: str = 'date', 
             min_length: int = 5, 
             max_length: int = 500, 
             start_date: str = '1900-01-01', 
             end_date: str = '2100-12-31',
             sequence_of_operations: list = None,
             mapping_label: dict = None,
             semantic_task: str = 'sentiment',
             semantic_model_name: str = None) -> dict:
    """
    Calculates the overall accuracy of a dataset by evaluating syntactic accuracy, data model accuracy,
    risk of inaccuracy, and semantic accuracy.

    Parameters:
    - df (pd.DataFrame): The input dataframe.
    - required_columns (list): List of required column names.
    - required_size (int): Minimum required number of rows.
    - text_column (str): Name of the text column. Default is 'text'.
    - date_column (str): Name of the date column. Default is 'date'.
    - min_length (int): Minimum allowed length for text entries. Default is 5.
    - max_length (int): Maximum allowed length for text entries. Default is 500.
    - start_date (str): Earliest allowed date. Default is '1900-01-01'.
    - end_date (str): Latest allowed date. Default is '2100-12-31'.
    - sequence_of_operations (list): List of text processing operations. Default is None.
    - mapping_label (dict): Dictionary mapping model predictions to dataset labels for semantic accuracy.
    - semantic_task (str): Either 'sentiment' or 'news' to select the appropriate semantic model. Default is 'sentiment'.
    - semantic_model_name (str): The model name to use for semantic prediction. Default is None.

    Returns:
    - dict: A JSON-formatted string summarizing the overall accuracy results.
    """
    accuracy_result = {}

    # Step 1: Check syntactic accuracy (e.g., removing links, phone numbers, extra spaces)
    syntactic_accuracy = SyntacticAccuracy(df, text_column=text_column, 
                                           sequence_of_operations=sequence_of_operations)
    syntactic_accuracy_report = syntactic_accuracy.get_syntactic_accuracy()

    # Step 2: Check data model accuracy (validates column presence and row count)
    model_accuracy = DataModelAccuracy(df, required_columns, required_size)
    model_accuracy.check_columns()
    model_accuracy.check_rows()
    model_accuracy_report = model_accuracy.get_model_accuracy()

    # Step 3: Assess risk of inaccuracy (checks text length and date validity)
    risk_checker = RiskOfInaccuracy(df, text_column=text_column, date_column=date_column, 
                                    min_length=min_length, max_length=max_length, 
                                    start_date=start_date, end_date=end_date)
    risk_checker.check_text_length()
    risk_checker.check_date_validity()
    risk_checker_report = risk_checker.get_risk_assessment()

    # Step 4: Check semantic accuracy if mapping_label is provided
    # Semantic accuracy compares the predicted labels with the actual labels.
    if mapping_label is not None:
        semantic_accuracy_report = SemanticACcuracy(df, mapping_label, 
                                                    text_column=text_column, 
                                                    label_column='label', 
                                                    task=semantic_task, 
                                                    model_name=semantic_model_name)
        accuracy_result["semantic_accuracy"] = json.loads(semantic_accuracy_report)

    # Combine all reports into the final accuracy result.
    # Ensure reports are converted to dictionaries from JSON strings.
    accuracy_result["syntactic_accuracy"] = json.loads(syntactic_accuracy_report)
    accuracy_result["model_accuracy"] = json.loads(model_accuracy_report)
    accuracy_result["risk_assessment"] = json.loads(risk_checker_report)

    return json.dumps(accuracy_result, ensure_ascii=False, indent=4)


# ----------------- Example Usage -----------------

# Example data for Farsi Sentiment Dataset (adding an 'id' column to meet required_columns)
# data = {
#     "id": [1, 2, 3],
#     "text": [
#         "این یک محصول عالی است                 ",  # Positive sentiment
#         "کیفیت خیلی بد بود، ناراضی هستم",             # Negative sentiment
#         "محصول"                                     # Neutral sentiment (too short)
#     ],
#     "label": ["عالی", "منفی", "خنثی"],
#     "date": ["2024-01-01", "2024-01-02", "1990-01-03"]
# }

# df = pd.DataFrame(data)
# required_columns = ["id", "text", "label", "date"]
# required_size = 3  # Adjusted to match the sample data size

# # Mapping for semantic accuracy (for sentiment analysis)
# mapping_label = {
#     "furious": "خشمگین",
#     "angry": "عصبانی",
#     "neutral": "خنثی",
#     "happy": "خوشحال",
#     "delighted": "عالی"
# }

# # Calculate overall accuracy including syntactic, data model, risk, and semantic accuracy.
# accuracy_result = accuracy(df, 
#                            required_columns, 
#                            required_size, 
#                            text_column="text", 
#                            date_column="date", 
#                            min_length=5, 
#                            max_length=50, 
#                            start_date="2024-01-01", 
#                            end_date="2024-12-31",
#                            sequence_of_operations=["remove_links", "remove_phone_numbers", "remove_extra_spaces"],
#                            mapping_label=mapping_label,
#                            semantic_task='sentiment',
#                            semantic_model_name="deepsentipers")

# print(accuracy_result)


# output

# {
#     "semantic_accuracy": {
#         "accuracy": 0.6666666666666666,
#         "conflicts": [
#             {
#                 "index": 1,
#                 "text": "کیفیت خیلی بد بود، ناراضی هستم",
#                 "actual_label": "منفی",
#                 "predicted_label": "عصبانی"
#             }
#         ]
#     },
#     "syntactic_accuracy": {
#         "accuracy": 0.3333333333333333,
#         "problematic_data": {
#             "remove_extra_spaces": [
#                 "این یک محصول عالی است                 "
#             ]
#         }
#     },
#     "model_accuracy": {
#         "accuracy_scores": {
#             "column_presence": 1.0,
#             "size_requirement": 1.0
#         },
#         "overall_accuracy": 1.0,
#         "missing_columns": []
#     },
#     "risk_assessment": {
#         "risk_scores": {
#             "text_length": 1.0,
#             "date_validity": 0.67
#         },
#         "average_risk": 0.83,
#         "outlier_texts": [],
#         "outlier_dates": [
#             "1990-01-03"
#         ]
#     }
# }