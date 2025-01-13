# Early Dropout Prediction System

## Project Overview
The **Early Dropout Prediction System (EDPS)** is a machine learning-based tool designed to identify students at risk of dropping out of their educational programs. By leveraging predictive models trained on student data, EDPS provides early interventions to improve retention rates and overall student success.

## Features
- Predicts dropout risk using multiple classifiers, including Random Forest, K-Nearest Neighbors (KNN), and Logistic Regression.
- Supports K-Fold Cross-Validation for robust model evaluation.
- Handles missing data using imputation techniques.
- Provides feature importance insights to explain predictions (Random Forest).
- Prepares and preprocesses datasets for training, validation, and testing.

## Installation
To get started with the Early Dropout Prediction System, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://gitlab.eeecs.qub.ac.uk/40328713/early-dropout-prediction-system.git
    cd early-dropout-prediction-system
    ```

2. Set up a Python virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For Linux/MacOS
    venv\Scripts\activate  # For Windows
    ```

3. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure you have the necessary datasets in the `data/processed/` directory:
    - `train_dataset.csv`
    - `validate_dataset.csv`
    - `test_dataset.csv`

## Usage

### Training Models
Three classifiers are currently implemented:

1. **Random Forest**
    ```bash
    python scripts/train_randomforest.py
    ```

2. **K-Nearest Neighbors (KNN)**
    ```bash
    python scripts/train_knn.py
    ```

3. **Logistic Regression**
    ```bash
    python scripts/train_logistic_regression.py
    ```

Each script performs training, evaluation on the validation set, and final testing, saving the trained model to the `models/` directory.

### Optimizing Hyperparameters
To find the optimal parameters for Random Forest (e.g., the number of trees):
```bash
python scripts/optimise_randtrees.py
```

### Preprocessing Data
Ensure your raw datasets are preprocessed:
```bash
python scripts/test_preprocess.py
```

### Making Predictions
To make predictions on new datasets (e.g., enrolled students):
```bash
python scripts/enrolled_prediction.py
```

## Project Structure
```
.
├── data
│   ├── processed
│   │   ├── train_dataset.csv
│   │   ├── validate_dataset.csv
│   │   ├── test_dataset.csv
│   └── raw
├── models
│   ├── random_forest
│   ├── knn
│   └── logistic_regression
├── pipeline
│   ├── preprocess_student_dropout_data.py
│   ├── train_randomforest.py
│   ├── train_knn.py
│   ├── train_logistic_regression.py
├── scripts
│   ├── optimise_randtrees.py
│   ├── test_preprocess.py
│   ├── enrolled_prediction.py
├── README.md
├── requirements.txt
└── ...
```

## Dependencies
- Python 3.8+
- pandas
- scikit-learn
- joblib
- numpy

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Roadmap
- [ ] Implement additional classifiers (e.g., Gradient Boosting, Support Vector Machines).
- [ ] Add advanced hyperparameter optimization (e.g., Bayesian optimization).
- [ ] Provide a web-based interface for uploading data and viewing predictions.
- [ ] Enhance feature engineering capabilities for better prediction performance.

## Contributing
We welcome contributions to enhance the Early Dropout Prediction System. Please follow these steps:
1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes and push to your branch.
4. Create a merge request on GitLab.

## Authors
- **Andrew Hyde**

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- **Supervisor**: Baharak Ahmaderaghi
- **Queen's University Belfast**
