"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""


from .utils import CleanText
import torch
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import json
from transformers import BertTokenizer, BertModel

class SyntacticAccuracy:
    """
    Class to calculate syntactic accuracy of text data by validating the alignment 
    of the text with a sequence of cleaning operations, and measuring the similarity 
    before and after the cleaning process.

    Parameters:
    - df: Pandas DataFrame containing the dataset with text data.
    - text_column: The column name in the DataFrame containing the text to be processed (default is 'text').
    - sequence_of_operations: List of text cleaning operations to apply on the data (default is an empty list).
    - threshold: The threshold value for similarity calculation (default is 0.7). This value can be used 
                to filter texts that are significantly changed after cleaning.
    """

    def __init__(self, df: pd.DataFrame, text_column='text', sequence_of_operations: list = None, threshold: float = 0.7):
        """
        Initialize the SyntacticAccuracy class with required parameters and resources.

        Parameters:
        - df: Pandas DataFrame containing the text data to be processed.
        - text_column: The column name where the text data is located (default is 'text').
        - sequence_of_operations: A list of cleaning operations to apply in sequence.
        - threshold: A threshold for similarity calculation between the original and cleaned text.
        """
        self.threshold = threshold
        
        self.df = df        
        self.text_column = text_column
        self.sequence_of_operations = sequence_of_operations if sequence_of_operations else []        
        self.CleanText = CleanText()
        
        self.operations_map = {
            "remove_links": self.CleanText.remove_links, 
            "remove_emails": self.CleanText.remove_emails,
            "remove_hashtags": self.CleanText.remove_hashtags,
            "remove_mentions": self.CleanText.remove_mentions,
            "remove_phone_numbers": self.CleanText.remove_phone_numbers,
            "remove_persian_punctuation": self.CleanText.remove_persian_punctuation,
            "remove_arabic_diacritics": self.CleanText.remove_arabic_diacritics,
            "remove_informal_words": self.CleanText.remove_informal_words,
            "remove_stopwords": self.CleanText.remove_stopwords,
            "remove_extra_spaces": self.CleanText.remove_extra_spaces,
            "remove_emoji": self.CleanText.remove_emoji
        }
        
        self.tokenizer = BertTokenizer.from_pretrained('HooshvareLab/bert-base-parsbert-uncased')
        self.model = BertModel.from_pretrained('HooshvareLab/bert-base-parsbert-uncased')

    def validate_text(self, text: str) -> tuple:
        """
        Validate and clean the input text based on the specified operations.

        Parameters:
        - text: The input text that needs to be cleaned and validated.

        Returns:
        - cleaned_text: The cleaned version of the original text after applying the operations.
        - problematic_issues: A dictionary containing the cleaning operations that modified the text.
        """
        problematic_issues = {}
        
        cleaned_text = text
        
        for operation in self.sequence_of_operations:
            if operation in self.operations_map:
                new_text = self.operations_map[operation](cleaned_text)
                
                if new_text != cleaned_text:
                    if operation not in problematic_issues:
                        problematic_issues[operation] = []
                    problematic_issues[operation].append(text)
                
                cleaned_text = new_text
        
        return cleaned_text, problematic_issues

    def get_bert_embedding(self, text: str) -> torch.Tensor:
        """
        Get the BERT embedding (vector representation) for a given text.

        Parameters:
        - text: The input text for which the embedding is to be generated.

        Returns:
        - embeddings: A tensor representing the BERT embedding of the input text.
        """
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1)
        
        return embeddings

    def calculate_similarity(self, original_text: str, cleaned_text: str) -> float:
        """
        Calculate the cosine similarity between the original and cleaned text embeddings.

        Parameters:
        - original_text: The original input text.
        - cleaned_text: The cleaned version of the input text.

        Returns:
        - similarity: The cosine similarity score between the original and cleaned text.
        """
        original_embedding = self.get_bert_embedding(original_text)
        cleaned_embedding = self.get_bert_embedding(cleaned_text)
        
        similarity = cosine_similarity(original_embedding.numpy(), cleaned_embedding.numpy())[0][0]
        
        return similarity

    def get_syntactic_accuracy(self) -> str:
        """
        Calculate the syntactic accuracy for the entire dataset by measuring the similarity 
        between the original and cleaned text for each row. It also generates a report of 
        problematic operations that modified the text.

        Returns:
        - result: A JSON string containing the overall accuracy and problematic data.
        """
        similarities = []
        
        issue_report = {key: [] for key in self.operations_map.keys()}
        
        # Iterate through each row in the dataframe
        for _, row in self.df.iterrows():
            # Get the original text from the dataframe
            original_text = row[self.text_column]
            
            cleaned_text, problematic_issues = self.validate_text(original_text)
            
            similarity_score = self.calculate_similarity(original_text, cleaned_text)
            similarities.append(similarity_score)
            
            for issue, texts in problematic_issues.items():
                issue_report[issue].extend(texts)
        print(issue_report)
        accuracy = 1 / len(self.df)
        
        result = {
            "accuracy": accuracy,  # Overall syntactic accuracy
            "problematic_data": {key: list(set(value)) for key, value in issue_report.items() if value}  # Problematic operations with the respective texts
        }
        
        return json.dumps(result, ensure_ascii=False, indent=4)


# Example usage
# data = {
#     "text": [
#         "https://github.com/ItrcAiLabs/data-validation/tree/main/textاین یک محصول عالی است",
#         "کیفیت خیلی بد بود، ناراضی هستم",
#         "محصول متوسط بود، می‌توانست بهتر باشد",
#     ],
#     "label": ["مثبت", "منفی", "خنثی"],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03"]
# }

# df = pd.DataFrame(data)

# syntactic_accuracy = SyntacticAccuracy(df, text_column="text", sequence_of_operations=["remove_links", "remove_phone_numbers", "remove_extra_spaces"])
# accuracy_report = syntactic_accuracy.get_syntactic_accuracy()
# print(accuracy_report)


# output
    # {
    #     "accuracy": 0.8476517995198568,
    #     "problematic_data": {
    #         "remove_links": [
    #             "https://github.com/ItrcAiLabs/data-validation/tree/main/textاین یک محصول عالی است"
    #         ],
    #         "remove_extra_spaces": [
    #             "https://github.com/ItrcAiLabs/data-validation/tree/main/textاین یک محصول عالی است"
    #         ]
    #     }
    # }