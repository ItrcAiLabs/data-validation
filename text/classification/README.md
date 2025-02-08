# Text Data Validation

## Overview
The `text` directory contains modules for validating text data based on multiple quality dimensions. These include classification accuracy, completeness, consistency, and currentness. Each module provides scripts to assess different aspects of data validation, ensuring the integrity and reliability of textual information.

## Directory Structure
```
text
├── classification
│   ├── accuracy
│   │   ├── cache
│   │   │   └── dadmatools
│   │   │       ├── fa_tokenizer
│   │   │       │   └── fa_tokenizer.pt
│   │   │       └── fa_tokenizer.pt
│   │   ├── data_model_accuracy.py
│   │   ├── risk_of_inaccuracy.py
│   │   ├── semantic_accuracy
│   │   │   ├── llm
│   │   │   │   └── llm.py
│   │   │   └── models
│   │   │       ├── political
│   │   │       └── sentiment_analysis
│   │   │           └── Pbert.py
│   │   ├── semantic_accuracy.py
│   │   ├── syntactic_accuracy.py
│   │   └── utils.py
│   ├── completeness
│   │   ├── feature_completeness.py
│   │   ├── record_completeness.py
│   │   └── value_occurrence_completeness.py
│   ├── consistency
│   │   ├── data_format_consistency.py
│   │   ├── data_record_consistency.py
│   │   ├── data_value_distribution.py
│   │   └── semantic_consistency.py
│   └── currentness
│       ├── record_currentness.py
│       └── utils.py
├── requirements.txt
```

## Modules

### 1. Classification
This module evaluates the accuracy of text classification models. It includes:
- **Accuracy**: Measures the correctness of predictions.
- **Semantic Accuracy**: Evaluates the meaning preservation in classifications.
- **Syntactic Accuracy**: Checks structural correctness.
- **Risk of Inaccuracy**: Estimates potential classification risks.

### 2. Completeness
Ensures that the dataset contains all necessary information. It includes:
- **Feature Completeness**: Verifies that required features exist.
- **Record Completeness**: Ensures no missing records.
- **Value Occurrence Completeness**: Checks for missing values in fields.

### 3. Consistency
Examines whether data is internally consistent across different records and formats. It includes:
- **Data Format Consistency**: Ensures data adheres to predefined formats.
- **Data Record Consistency**: Checks consistency between different records.
- **Data Value Distribution**: Analyzes statistical distribution of values.
- **Semantic Consistency**: Ensures logical consistency across text data.

### 4. Currentness
Validates whether data is up-to-date. It includes:
- **Record Currentness**: Checks if records are still relevant.
- **Utils**: Helper functions for currentness validation.

## Installation
To install required dependencies, run:
```sh
pip install -r requirements.txt
```

## Usage
Each script can be executed individually. For example, to run the `record_currentness.py` script:
```sh
python text/currentness/record_currentness.py
```

## Contributing
If you'd like to contribute, please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test them.
4. Submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For questions or suggestions, please contact the maintainers.

