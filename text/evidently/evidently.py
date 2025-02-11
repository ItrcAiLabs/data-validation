import pandas as pd

from typing import Optional
from typing import Dict
from typing import Generator
from typing import Union

from evidently.features.llm_judge import BinaryClassificationPromptTemplate

from evidently.future.datasets import Dataset
from evidently.future.datasets import DataDefinition
from evidently.future.datasets import DatasetColumn
from evidently.future.datasets import Descriptor

from evidently.future.descriptors import (
    TextLength,
    BERTScore,
    BeginsWith,
    Contains,
    ContainsLink,
    CustomColumnDescriptor,
    CustomDescriptor,
    DoesNotContain,
    EndsWith,
    ExactMatch,
    ExcludesWords,
    HuggingFace,
    HuggingFaceToxicity,
    IncludesWords,
    IsValidJSON,
    IsValidPython,
    IsValidSQL,
    JSONSchemaMatch,
    JSONMatch,
    LLMEval,
    NegativityLLMEval,
    PIILLMEval,
    DeclineLLMEval,
    BiasLLMEval,
    ToxicityLLMEval,
    ContextQualityLLMEval,
    ItemMatch,
    ItemNoMatch,
    NonLetterCharacterPercentage,
    OOVWordsPercentage,
    OpenAI,
    RegExp,
    SemanticSimilarity,
    SentenceCount,
    Sentiment,
    TriggerWordsPresent,
    WordCount,
    WordMatch,
    WordNoMatch,)
import os 

os.environ["OPENAI_API_KEY"] = "your_openai_api_key"


class Evidently():
    
    def __init__(self,text_columns : string = None,numerical_columns : int=None,categorical_columns=None):
        
            self.data_definition = DataDefinition(
            text_columns = text_columns,
            numerical_columns = numerical_columns,
            categorical_columns = categorical_columns
        )
            self.openai_api = os.environ["OPENAI_API_KEY"]
        
    def syntax_validation(self, data,
                          columns_for_json_schema = None,expected_schema= None,
                          columns_for_python= None,
                          columns_for_SQL= None):
          
          """Descriptors that validate structured data formats or code syntax.
            IsValidJSON(): Checks if the text contains valid JSON.
            JSONSchemaMatch(): Verifies JSON structure against an expected schema.
            JSONMatch(): Compares JSON against a reference column.
            IsValidPython(): Validates Python code syntax.
            IsValidSQL(): Validates SQL query syntax"""
          
          syntax_validation = Dataset.from_pandas(
                pd.DataFrame(data),
                data_definition= self.data_definition,
                descriptors = [
                     
                     JSONSchemaMatch(columns_for_json_schema,expected_schema=expected_schema),
                     IsValidJSON(columns_for_json_schema,alias =f"Is Valid JSON for column: {columns_for_json_schema}"),
                    
                     IsValidPython(columns_for_python, alias = f"Is Valid JSON for column: {columns_for_python}"),

                     IsValidSQL(columns_for_SQL, alias = f"Is Valid SQL for column: {columns_for_SQL}"),
                ]
           ) 
          
          return syntax_validation.as_dataframe()
          
    def semantic_validation_for_qa(self,data,
                            question_column,
                            answer_columns):
        """Descriptors that check for presence of specific words, items or components.

            Contains(): Checks if text contains specific items.
            DoesNotContain(): Ensures text does not contain specific items.
            IncludesWords(): Checks if text includes specific vocabulary words. #to be merged with Contains later
            ExcludesWords(): Ensures text excludes specific vocabulary words. #to be merged with DoesNotContain later
            ItemMatch(): Checks if text contains items from a separate column.
            ItemNoMatch(): Ensures text excludes items from a separate column.
            WordMatch(): Checks if text includes words from a separate column. #to be merged with ItemMatch later
            WordNoMatch(): Ensures text excludes words from a separate column. #to be merged with ItemNoMatch later
            ContainsLink(): Checks if text contains at least one valid URL."""
          

        semantic_check =   Dataset.from_pandas(
                pd.DataFrame(data),
                data_definition= self.data_definition,
                descriptors=[
                      SemanticSimilarity(columns=[question_column,answer_columns]),
                      IncludesWords(question_column,["کی","کجا"]),
                      ContainsLink(answer_columns)
                ]
          )    
        return semantic_check.as_dataframe()
    
    def llm_as_a_judge(self,data):
          
          llm_eval = Dataset.from_pandas(
                pd.DataFrame(data),
                data_definition=self.data_definition,
                descriptors=[
                     NegativityLLMEval("Answer"),
                     DeclineLLMEval("Answer"),
                     BiasLLMEval("Answer"),
                     ToxicityLLMEval("Answer"),
                     ContextQualityLLMEval("Answer", question="Question"), #here answer substitutes a context, cause there is no context 
                ]

                
          )



