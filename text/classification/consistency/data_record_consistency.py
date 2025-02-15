"""
    This code is written based on:  
        - ISO/IEC 5259, 25012, and 25024 standards.
"""

import pandas as pd
import json
import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

class DataRecordConsistency:
    def __init__(self, df: pd.DataFrame, similarity_threshold: float = 0.9) -> None:
        self.df = df.reset_index(drop=True)
        self.similarity_threshold = similarity_threshold
        self.duplicate_records = pd.DataFrame()
        self.duplicate_record_ratio = 0.0
        
        # Load Persian BERT model
        self.tokenizer = BertTokenizer.from_pretrained("HooshvareLab/bert-fa-base-uncased")
        self.model = BertModel.from_pretrained("HooshvareLab/bert-fa-base-uncased")
        self.model.eval()
    
    def evaluate_consistency(self) -> None:
        """Identifies exact and semantic duplicates"""
        # Find exact duplicates
        exact_dups = self.df[self.df.duplicated(keep=False)]
        
        # Find semantic duplicates
        embeddings = []
        for text in self.df['text']:
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                truncation=True,
                padding='max_length',
                max_length=128
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Fix dimension issue by squeezing
            emb = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            embeddings.append(emb)
        
        # Convert to proper 2D array
        embeddings = np.array(embeddings)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Find semantic duplicates
        semantic_dups = set()
        n = len(self.df)
        for i in range(n):
            for j in range(i+1, n):
                if similarity_matrix[i][j] > self.similarity_threshold:
                    semantic_dups.update([i, j])
        
        # Combine duplicates
        all_dups = exact_dups.index.union(semantic_dups).tolist()
        self.duplicate_records = self.df.loc[all_dups]
        self.duplicate_record_ratio = len(all_dups)/len(self.df) if len(self.df) > 0 else 0

    def get_consistency_report(self) -> str:
        """Generate JSON report with duplicates"""
        report = {
            "duplicate_ratio": round(self.duplicate_record_ratio, 2),
            "total_records": len(self.df),
            "duplicate_count": len(self.duplicate_records),
            "duplicates": self.duplicate_records.to_dict(orient='records')
        }
        return json.dumps(report, ensure_ascii=False, indent=4, default=str)

# Example usage

# data = pd.DataFrame({
#     'text': [
#         "این فیلم واقعا فوق العاده بود", 
#         "این فیلم واقعا فوق العاده بود",
#         "این محصول اصلا خوب نیست",
#         "این محصول  خوب نیست",
#         "نظر من در مورد این فیلم مثبت است"
#     ],
#     'label': ["مثبت", "مثبت", "منفی", "منفی", "مثبت"],
#     'date': ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03"]
# })

# checker = DataRecordConsistency(data, similarity_threshold=0.85)
# checker.evaluate_consistency()
# print(checker.get_consistency_report())


# output

    # {
    #     "duplicate_ratio": 0.8,
    #     "total_records": 5,
    #     "duplicate_count": 4,
    #     "duplicates": [
    #         {
    #             "text": "این فیلم واقعا فوق العاده بود",
    #             "label": "مثبت",
    #             "date": "2024-01-01"
    #         },
    #         {
    #             "text": "این فیلم واقعا فوق العاده بود",
    #             "label": "مثبت",
    #             "date": "2024-01-01"
    #         },
    #         {
    #             "text": "این محصول اصلا خوب نیست",
    #             "label": "منفی",
    #             "date": "2024-01-02"
    #         },
    #         {
    #             "text": "این محصول  خوب نیست",
    #             "label": "منفی",
    #             "date": "2024-01-02"
    #         }
    #     ]
    # }