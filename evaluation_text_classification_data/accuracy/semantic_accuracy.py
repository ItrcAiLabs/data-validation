"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd
import json


from .SemanticAccuracy.models.news.Pbert import PersianNewsBERT
from .SemanticAccuracy.models.sentiment_analysis.Pbert import SentimentAnalysisBERT

def SemanticACcuracy(df, mapping_label, text_column='text', label_column='label', task='sentiment', model_name=None):
    """
    Calculate the semantic accuracy of labels in the dataset.
    
    Parameters:
    - df: DataFrame containing the data.
    - mapping_label: Dictionary mapping model predictions to dataset labels (user-provided).
    - text_column: Name of the column containing the text.
    - label_column: Name of the column containing the label.
    - task: Either 'sentiment' or 'news' to select the appropriate model.
    - model_name: The model name to use for prediction.
    
    Returns:
    - A dictionary containing the overall accuracy and a list of conflicting cases.
    """
    # Initialize the appropriate model based on the task type
    if task.lower() == 'sentiment':
        model = SentimentAnalysisBERT()
        if model_name is None:
            model_name = "deepsentipers"
    elif task.lower() == 'news':
        model = PersianNewsBERT()
        if model_name is None:
            model_name = "persiannews"
    else:
        raise ValueError("Invalid task type provided. Please use 'sentiment' or 'news'.")
    
    total = len(df)
    correct = 0
    conflicts = []
    
    # Iterate through each row and compare the predicted label with the actual label
    for idx, row in df.iterrows():
        text = row[text_column]
        actual_label = row[label_column]
        predicted_label = model.predict(text, mapping_label, model_name=model_name)
        
        if predicted_label == actual_label:
            correct += 1
        else:
            conflicts.append({
                "index": idx,
                "text": text,
                "actual_label": actual_label,
                "predicted_label": predicted_label
            })
    
    accuracy = correct / total if total > 0 else 0
    result = {
        "accuracy": accuracy,
        "conflicts": conflicts
    }
    
    return json.dumps(result, ensure_ascii=False, indent=4)


# ----------------- Example Usage -----------------


# Example for News Classification:
# mapping_label = {
#     "politics": "سیاست",
#     "economy": "اقتصاد",
#     "technology": "فناوری",
#     "culture": "فرهنگ",
#     "sports": "ورزش"
# }

# df_news = pd.DataFrame({
#     "text": [
#         "این یک خبر در زمینه اقتصاد است.",
#         "خبر دیگری در زمینه سیاست.",
#         "خبر فناوری جدید منتشر شد."
#     ],
#     "label": [
#         "اقتصاد",
#         "سیاست",
#         "فناوری"
#     ],
#     "date": [
#         "2024-02-01",
#         "2024-02-02",
#         "2024-02-03"
#     ]
# })

# result_news = SemanticACcuracy(df_news, mapping_label, task='news', model_name="persiannews")
# print(result_news)

#out put
# {
#     "accuracy": 0.3333333333333333,
#     "conflicts": [
#         {
#             "index": 1,
#             "text": "خبر دیگری در زمینه سیاست.",
#             "actual_label": "سیاست",
#             "predicted_label": "فرهنگ"
#         },
#         {
#             "index": 2,
#             "text": "خبر فناوری جدید منتشر شد.",
#             "actual_label": "فناوری",
#             "predicted_label": "ورزش"
#         }
#     ]
# }