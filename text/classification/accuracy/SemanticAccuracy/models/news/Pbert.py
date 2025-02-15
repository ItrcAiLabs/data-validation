from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Acceptable:
    def __init__(self, labels):
        self.labels = labels

    def get_label(self, prediction, mapping_label):
        prediction = self.labels[prediction]
        return mapping_label.get(prediction, prediction)


class PersianNewsBERT:
    def __init__(self):
        # Initialize tokenizers, models, and acceptable classes for different datasets
        self.models = {
            "persiannews": {
                "tokenizer": AutoTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased-clf-persiannews"),
                "model": AutoModelForSequenceClassification.from_pretrained("HooshvareLab/bert-fa-base-uncased-clf-persiannews"),
                "acceptable": Acceptable(["politics", "economy", "technology", "culture", "sports"])
            }
        }

    def predict(self, text, mapping_label: dict, model_name="persiannews"):
        """Predict category using the specified model."""
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
        predicted_label = acceptable.get_label(predicted_class, mapping_label)

        return predicted_label


# Example usage:

# persian_news_bert = PersianNewsBERT()
# text = "این یک خبر در زمینه اقتصاد است."
# mapping_label = {
#                 "politics": "سیاست",
#                 "economy": "اقتصاد",
#                 "technology": "فناوری",
#                 "culture": "فرهنگ",
#                 "sports": "ورزش"
#             }
# prediction = persian_news_bert.predict(text, mapping_label, model_name="persiannews")
# print(f"Predicted category: {prediction}")

# Predicted category: اقتصاد