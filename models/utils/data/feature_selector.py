import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, chi2

def find_optimal_k(feature_importances, threshold=0.95):
    """
    Finds the smallest k where the cumulative sum of feature importances 
    reaches a defined threshold (default 95% of importance).

    Parameters:
        feature_importances (array-like): Importance scores of features.
        threshold (float): The percentage of importance to retain (0-1).

    Returns:
        int: Optimal number of features (k).

    Raises:
        ValueError: If threshold is not between 0 and 1 or if feature_importances is empty.
    """
    if not 0 < threshold < 1:
        raise ValueError("Threshold must be between 0 and 1 (non-inclusive).")
    if feature_importances is None or len(feature_importances) == 0:
        raise ValueError("Feature importances array is empty.")

    sorted_importances = np.sort(feature_importances)[::-1]  # Sort in descending order
    cumulative_importance = np.cumsum(sorted_importances)
    optimal_k = np.argmax(cumulative_importance >= threshold) + 1  # Smallest k covering threshold
    return optimal_k


def remove_highly_correlated_features(combined_df, threshold=0.85):
    """
    Removes highly correlated features to reduce redundancy.
    
    Parameters:
        combined_df (pd.DataFrame): The combined dataset.
        threshold (float): The correlation threshold for removing features.

    Returns:
        pd.DataFrame: The dataset with reduced multicollinearity.

    Raises:
        ValueError: If the provided dataframe is empty.
    """
    if combined_df is None or combined_df.empty:
        raise ValueError("Input dataframe is empty.")

    # Select only numerical features for correlation analysis
    numeric_df = combined_df.select_dtypes(include=[np.number])
    if numeric_df.empty:
        print("⚠️ No numerical features available for correlation analysis.")
        return combined_df

    # Compute the correlation matrix
    corr_matrix = numeric_df.corr().abs()

    # Select the upper triangle of the correlation matrix
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Identify features with correlation higher than the threshold
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]

    if to_drop:
        print(f"🔍 Removing {len(to_drop)} highly correlated features: {to_drop}")
    else:
        print("🔍 No highly correlated features found to remove.")

    # Drop the highly correlated columns (ignore errors if a column is missing)
    df_reduced = combined_df.drop(columns=to_drop, errors='ignore')
    return df_reduced


def select_best_features(combined_df, target_column="target", importance_threshold=0.95):
    """
    Dynamically selects the best features using ANOVA F-Test for numerical features 
    and Chi-Square Test for categorical features.

    Parameters:
        combined_df (pd.DataFrame): The dataset.
        target_column (str): The target variable.
        importance_threshold (float): The percentage of feature importance to retain.

    Returns:
        pd.DataFrame: Dataset with selected features.

    Raises:
        ValueError: If the target column is missing or no features are selected.
    """
    # Check if target column exists
    if target_column not in combined_df.columns:
        raise ValueError(f"target column '{target_column}' is not present in the dataset.")

    # Drop non-relevant columns (e.g., "dataset_marker") if present
    if "dataset_marker" in combined_df.columns:
        combined_df = combined_df.drop(columns=["dataset_marker"])

    # Separate features and target
    try:
        X = combined_df.drop(columns=[target_column])
    except KeyError:
        raise ValueError(f"target column '{target_column}' not found in dataset.")
    y = combined_df[target_column]

    if X.empty:
        raise ValueError("Feature set is empty after dropping the target column.")
    
    # Identify numerical and categorical features
    numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()
    categorical_features = X.select_dtypes(include=["object"]).columns.tolist()

    selected_features = []

    print(f"🔍 Before feature selection: {len(numerical_features)} numerical, {len(categorical_features)} categorical features")

    # Apply ANOVA F-Test for numerical features
    if numerical_features:
        try:
            selector = SelectKBest(score_func=f_classif, k="all")
            selector.fit(X[numerical_features], y)
        except Exception as e:
            raise RuntimeError(f"Error during ANOVA F-Test: {e}")

        # Log numerical feature importance scores
        feature_scores = dict(zip(numerical_features, selector.scores_))
        print("\n🔍 Numerical Feature Importance Scores (Before Selection):")
        for feat, score in sorted(feature_scores.items(), key=lambda x: x[1], reverse=True):
            print(f"{feat}: {score:.4f}")

        try:
            k_num = find_optimal_k(selector.scores_, importance_threshold)
            k_num = max(10, k_num)  # Ensure at least 10 numerical features are kept
            selector = SelectKBest(score_func=f_classif, k=min(k_num, len(numerical_features)))
            selector.fit(X[numerical_features], y)
            selected_num_features = np.array(numerical_features)[selector.get_support()].tolist()
            selected_features.extend(selected_num_features)
        except Exception as e:
            print(f"⚠️ Issue selecting numerical features: {e}")

    # Apply Chi-Square Test for categorical features
    if categorical_features:
        try:
            selector = SelectKBest(score_func=chi2, k="all")
            # Convert categorical features to integer codes
            X_categorical_filtered = X[categorical_features].apply(lambda col: col.astype("category").cat.codes)
            selector.fit(X_categorical_filtered, y)
        except Exception as e:
            print(f"⚠️ Error during Chi-Square test for categorical features: {e}")
            X_categorical_filtered = pd.DataFrame()

        if not X_categorical_filtered.empty:
            # Log categorical feature importance scores
            feature_scores = dict(zip(categorical_features, selector.scores_))
            print("\n🔍 Categorical Feature Importance Scores (Before Selection):")
            for feat, score in sorted(feature_scores.items(), key=lambda x: x[1], reverse=True):
                print(f"{feat}: {score:.4f}")

            try:
                k_cat = find_optimal_k(selector.scores_, importance_threshold)
                k_cat = max(5, k_cat)  # Ensure at least 5 categorical features are kept
                selector = SelectKBest(score_func=chi2, k=min(k_cat, len(categorical_features)))
                selector.fit(X_categorical_filtered, y)
                selected_cat_features = np.array(categorical_features)[selector.get_support()].tolist()
                selected_features.extend(selected_cat_features)
            except Exception as e:
                print(f"⚠️ Issue selecting categorical features: {e}")

    if not selected_features:
        raise ValueError("No features were selected. Please check the input data and target column.")

    selected_df = combined_df[selected_features + [target_column]]
    print(f"\n✅ Selected {len(selected_features)} best features: {selected_features}")
    return selected_df
