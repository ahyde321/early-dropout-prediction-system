import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, chi2

def find_optimal_k(feature_importances, threshold=0.95):
    """
    Finds the smallest k where the cumulative sum of feature importances 
    reaches a defined threshold (default 95% of importance).

    Parameters:
    feature_importances (array): Importance scores of features.
    threshold (float): The percentage of importance to retain.

    Returns:
    int: Optimal number of features (k).
    """
    sorted_importances = np.sort(feature_importances)[::-1]  # Sort in descending order
    cumulative_importance = np.cumsum(sorted_importances)
    optimal_k = np.argmax(cumulative_importance >= threshold) + 1  # Smallest k covering 95% of importance
    return optimal_k


def remove_highly_correlated_features(combined_df, threshold=0.85):
    """
    Removes highly correlated features to reduce redundancy.

    Parameters:
    combined_df (pd.DataFrame): The combined dataset.
    threshold (float): The correlation threshold for removing features.

    Returns:
    pd.DataFrame: The dataset with reduced multicollinearity.
    """
    # Select only numerical features for correlation analysis
    numeric_df = combined_df.select_dtypes(include=[np.number])

    # Compute the correlation matrix
    corr_matrix = numeric_df.corr().abs()

    # Select the upper triangle of the correlation matrix
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Identify features with correlation higher than the threshold
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]

    # Drop the highly correlated columns
    df_reduced = combined_df.drop(columns=to_drop)

    print(f"🔍 Removed {len(to_drop)} highly correlated features: {to_drop}")
    return df_reduced



def select_best_features(combined_df, target_column="Target", importance_threshold=0.95):
    """
    Dynamically selects the best features using ANOVA F-Test for numerical 
    and Chi-Square Test for categorical features.

    Parameters:
    combined_df (pd.DataFrame): The dataset.
    target_column (str): The target variable.
    importance_threshold (float): The percentage of feature importance to retain.

    Returns:
    pd.DataFrame: Dataset with selected features.
    """
    # Drop non-relevant columns (e.g., "dataset_marker")
    if "dataset_marker" in combined_df.columns:
        combined_df = combined_df.drop(columns=["dataset_marker"])

    # Separate features from target
    X = combined_df.drop(columns=[target_column])
    y = combined_df[target_column]

    # Identify numerical and categorical features
    numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    selected_features = []

    # Log how many features we have before selection
    print(f"🔍 Before feature selection: {len(numerical_features)} numerical, {len(categorical_features)} categorical features")

    # Apply ANOVA F-Test for numerical features
    if numerical_features:
        selector = SelectKBest(score_func=f_classif, k="all")
        selector.fit(X[numerical_features], y)

        # Log importance scores for debugging
        feature_scores = dict(zip(numerical_features, selector.scores_))
        print("\n🔍 Numerical Feature Importance Scores (Before Selection):")
        for feat, score in sorted(feature_scores.items(), key=lambda x: x[1], reverse=True):
            print(f"{feat}: {score:.4f}")

        # Find optimal k
        k_num = find_optimal_k(selector.scores_, importance_threshold)
        k_num = max(10, k_num)  # Ensure at least 10 numerical features are kept

        selector = SelectKBest(score_func=f_classif, k=min(k_num, len(numerical_features)))
        X_num_selected = selector.fit_transform(X[numerical_features], y)
        selected_num_features = np.array(numerical_features)[selector.get_support()].tolist()
        selected_features.extend(selected_num_features)

    # Apply Chi-Square Test for categorical features
    if categorical_features:
        selector = SelectKBest(score_func=chi2, k="all")

        # Ensure categorical features contain valid integer values
        X_categorical_filtered = X[categorical_features].apply(lambda col: col.astype("category").cat.codes)

        selector.fit(X_categorical_filtered, y)

        # Log importance scores for debugging
        feature_scores = dict(zip(categorical_features, selector.scores_))
        print("\n🔍 Categorical Feature Importance Scores (Before Selection):")
        for feat, score in sorted(feature_scores.items(), key=lambda x: x[1], reverse=True):
            print(f"{feat}: {score:.4f}")

        # Find optimal k
        k_cat = find_optimal_k(selector.scores_, importance_threshold)
        k_cat = max(5, k_cat)  # Ensure at least 5 categorical features are kept

        selector = SelectKBest(score_func=chi2, k=min(k_cat, len(categorical_features)))
        X_cat_selected = selector.fit_transform(X_categorical_filtered, y)
        selected_cat_features = np.array(categorical_features)[selector.get_support()].tolist()
        selected_features.extend(selected_cat_features)


    # Keep only selected features
    selected_df = combined_df[selected_features + [target_column]]

    print(f"\n✅ Selected {len(selected_features)} best features: {selected_features}")
    return selected_df

