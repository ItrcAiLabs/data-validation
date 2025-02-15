"""
    This code is based on the Parse BERT models developed by Hooshvare Lab.

    For more information visit:
    URL: https://huggingface.co/HooshvareLab
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Acceptable:
    def __init__(self, labels):
        self.labels = labels

    def get_label(self, prediction, mapping_lable):
        
        prediction = self.labels[prediction]
        return mapping_lable[prediction]

class SentimentAnalysisBERT:
    def __init__(self):
        # Initialize tokenizers, models, and acceptable classes for different datasets
        self.models = {

            "snappfood": {
                "tokenizer": AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-snappfood"),
                "model": AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-snappfood"),
                "acceptable": Acceptable(["negative", "positive"])
            },
            "deepsentipers": {
                "tokenizer": AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-deepsentipers-multi"),
                "model": AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-sentiment-deepsentipers-multi"),
                "acceptable": Acceptable(["furious", "angry", "neutral", "happy", "delighted"])
            }
        }

    def predict(self, text, mapping_lable: dict, model_name="digikala",):
        """Predict sentiment using the specified model."""
        if model_name not in self.models:
            raise ValueError(f"Model '{model_name}' not found. Choose from {list(self.models.keys())}.")

        tokenizer = self.models[model_name]["tokenizer"]
        model = self.models[model_name]["model"]
        acceptable = self.models[model_name]["acceptable"]

        # Tokenize input text
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Perform inference
        with torch.no_grad():
            outputs = model(**inputs)

        # Get prediction
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

        # Map prediction to label
        predicted_label = acceptable.get_label(predicted_class, mapping_lable)

        return predicted_label

# Example usage:

# pbert = SentimentAnalysisBERT()
# text = "این یک محصول عالی است!"
# mapping_lable = {
#                 "furious": "خشمگین",
#                 "angry": "عصبانی",
#                 "neutral": "خنثی",
#                 "happy": "خوشحال",
#                 "delighted": "عالی"
#             }
# prediction = pbert.predict(text, mapping_lable, model_name="deepsentipers")
# print(f"Predicted sentiment: {prediction}")


# output
# Predicted sentiment: عالی