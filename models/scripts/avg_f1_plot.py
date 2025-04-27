import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 📊 F1-Scores from your results (Early, Mid, Final stages)

# Each model's F1-score at each stage
f1_scores = {
    "Random Forest": [0.8102, 0.9080, 0.9035],
    "XGBoost": [0.8258, 0.9144, 0.9038],
    "Logistic Regression": [0.7982, 0.9123, 0.9096],
    "K-Nearest Neighbours": [0.8034, 0.8979, 0.8997],
}

# 📈 Calculate average F1-Score for each model
average_f1_scores = {model: np.mean(scores) for model, scores in f1_scores.items()}

# Sort models by average F1-Score (optional, looks nice)
average_f1_scores = dict(sorted(average_f1_scores.items(), key=lambda item: item[1], reverse=True))

# Prepare data for plotting
models = list(average_f1_scores.keys())
avg_scores = list(average_f1_scores.values())

# 🎨 Create the plot
plt.figure(figsize=(8, 5))
sns.barplot(x=avg_scores, y=models)

for index, value in enumerate(avg_scores):
    plt.text(value + 0.002, index, f"{value:.4f}", va='center')

plt.title('Average F1-Score Across Early, Mid, and Final Stages')
plt.xlabel('Average F1-Score')
plt.xlim(0.75, 0.95)  # Optional: Adjust limits to focus on your F1 range
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
