"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd
import json
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
import torch
import numpy as np

class SemanticConsistency:
    def __init__(self, df: pd.DataFrame, text_column: str, label_column: str, date_column: str, model_name: str = "HooshvareLab/bert-fa-base-uncased", similarity_threshold: float = 0.9) -> None:
        """
        Initializes the SemanticConsistency object.

        Parameters:
        df (pd.DataFrame): The input dataframe containing the text data.
        text_column (str): The column in the dataframe containing the text to analyze.
        label_column (str): The column in the dataframe containing the labels for the text.
        date_column (str): The column in the dataframe containing the date of the texts.
        model_name (str): The name of the pre-trained BERT model to use for embedding generation.
        similarity_threshold (float): The cosine similarity threshold above which texts are considered semantically similar.
        """
        # Resetting index and initializing variables
        self.df = df.reset_index(drop=True)
        self.text_column = text_column
        self.label_column = label_column
        self.date_column = date_column
        self.invalid_indices = set()  # To store indices of rows with inconsistent semantics
        self.semantic_ratio = 0.0  # To store the semantic consistency ratio
        self.similarity_threshold = similarity_threshold  # Threshold for cosine similarity
        
        # Initialize the tokenizer and BERT model for Persian language
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
    
    def encode_text(self, text: str) -> torch.Tensor:
        """
        Converts a text to its BERT-based embedding representation.

        Parameters:
        text (str): The input text to be encoded.

        Returns:
        torch.Tensor: The average BERT embedding for the input text.
        """
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding='max_length', 
            max_length=128  # Limit the text length for shorter Persian texts
        )
        with torch.no_grad():
            # Get the embeddings (last hidden state) from the BERT model
            outputs = self.model(**inputs)
        return torch.mean(outputs.last_hidden_state, dim=1).squeeze()  # Return the average embedding

    def check_semantic_consistency(self) -> None:
        """
        Checks the semantic consistency of the text data by comparing the embeddings of texts.

        This function calculates the cosine similarity between the embeddings of all text pairs 
        and identifies any pairs of texts that are semantically similar but have different labels.
        """
        embeddings = []
        for text in self.df[self.text_column]:
            # Generate the BERT embeddings for each text in the dataframe
            emb = self.encode_text(text).numpy()
            embeddings.append(emb)
        embeddings = np.array(embeddings)
        
        # Compute the cosine similarity matrix between all text pairs
        similarity_matrix = cosine_similarity(embeddings)
        
        # Iterate through each pair of texts to find semantically similar pairs with different labels
        n = len(self.df)
        for i in range(n):
            for j in range(i + 1, n):
                # If the cosine similarity exceeds the threshold, check if the labels differ
                if similarity_matrix[i][j] > self.similarity_threshold:
                    if self.df.iloc[i][self.label_column] != self.df.iloc[j][self.label_column]:
                        # If they do, add their indices to the invalid indices set
                        self.invalid_indices.update([i, j])

    def get_semantic_consistency_report(self) -> str:
        """
        Generates a report on the semantic consistency of the text data.

        Returns:
        str: A JSON string containing the semantic consistency ratio, 
             the count of invalid rows, and details of the mismatched rows.
        """
        total_rows = len(self.df)
        invalid_count = len(self.invalid_indices)
        # Calculate the semantic consistency ratio (1 - proportion of invalid rows)
        self.semantic_ratio = round(1 - (invalid_count / total_rows), 2) if total_rows else 0.0
        
        mismatched_rows = []
        # For each invalid row, find its semantically similar rows
        for idx in self.invalid_indices:
            row = self.df.iloc[idx]
            similar = self._find_similar_texts(idx)
            if similar:  # Only include rows that have actual similar texts
                mismatched_rows.append({
                    "text": row[self.text_column],
                    "label": row[self.label_column],
                    "date": row[self.date_column],
                    "conflicts_with": similar
                })
        
        # Prepare the final result as a dictionary
        result = {
            "semantic_consistency_ratio": self.semantic_ratio,
            "mismatched_rows": mismatched_rows
        }
        # Return the result as a JSON-formatted string
        return json.dumps(result, ensure_ascii=False, indent=4, default=str)
    
    def _find_similar_texts(self, idx: int) -> list:
        """
        Finds semantically similar texts for a given row index.

        Parameters:
        idx (int): The index of the row whose similar texts need to be found.

        Returns:
        list: A list of similar texts with their labels, dates, and similarity scores.
        """
        similar = []
        target_embedding = self.encode_text(self.df.iloc[idx][self.text_column]).numpy()
        for i, row in self.df.iterrows():
            if i == idx:
                continue
            # Compute cosine similarity between the target text and the other texts
            sim = cosine_similarity([target_embedding], [self.encode_text(row[self.text_column]).numpy()])[0][0]
            # If similarity is above the threshold and labels are different, consider it similar
            if sim > self.similarity_threshold and row[self.label_column] != self.df.iloc[idx][self.label_column]:
                similar.append({
                    "text":row[self.text_column],
                    "label": row[self.label_column],
                    "date": row[self.date_column],
                    "similarity_score": float(sim)
                })
        return similar

# Example usage with sample data
# data = {
#     "text": [
#         "این یک محصول عالی است",
#         "کیفیت خیلی بد بود، ناراضی هستم",
#         "محصول متوسط بود، می‌توانست بهتر باشد",
#         "خرید این محصول را پیشنهاد نمی‌کنم",
#         "این یک محصول تقریبا عالی است"  
#     ],
#     "label": ["مثبت", "منفی", "خنثی", "منفی", "منفی"],
#     "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
# }
# df = pd.DataFrame(data)
# semantic_checker = SemanticConsistency(df, "text", "label", "date", similarity_threshold=0.95)
# semantic_checker.check_semantic_consistency()
# print(semantic_checker.get_semantic_consistency_report())

# output
    # {
    #     "semantic_consistency_ratio": 0.6,
    #     "mismatched_rows": [
    #         {
    #             "text": "این یک محصول عالی است",
    #             "label": "مثبت",
    #             "date": "2024-01-01",
    #             "conflicts_with": [
    #                 {
    #                     "text": "این یک محصول تقریبا عالی است",
    #                     "label": "منفی",
    #                     "date": "2024-01-05",
    #                     "similarity_score": 0.9799855947494507
    #                 }
    #             ]
    #         },
    #         {
    #             "text": "این یک محصول تقریبا عالی است",
    #             "label": "منفی",
    #             "date": "2024-01-05",
    #             "conflicts_with": [
    #                 {
    #                     "text": "این یک محصول عالی است",
    #                     "label": "مثبت",
    #                     "date": "2024-01-01",
    #                     "similarity_score": 0.9799855947494507
    #                 }
    #             ]
    #         }
    #     ]
    # }