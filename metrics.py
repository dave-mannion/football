import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    brier_score_loss,
    log_loss
)
from sklearn.calibration import calibration_curve
from typing import Union, List, Tuple


def median_calibration_error(
    y_true: Union[np.ndarray, pd.Series, List[int]],
    y_pred_proba: Union[np.ndarray, pd.Series, List[float]],
    n_bins: int = 100
) -> float:
    """
    Calculates the median calibration error.

    This metric assesses a model's calibration by dividing the predictions into
    percentile-based bins. For each bin, it calculates the difference between
    the mean predicted probability and the actual fraction of positives. The
    final metric is the median of these differences.

    A value closer to 0 indicates better calibration. A positive value
    suggests the model is, on average, over-confident in the bins, while a
    negative value suggests it is under-confident.

    Args:
        y_true (array-like):
            True binary labels (0 or 1).
        y_pred_proba (array-like):
            Predicted probabilities for the positive class (class 1).
        n_bins (int, optional):
            The number of bins to use, corresponding to percentiles.
            Defaults to 100 (one bin for each percentile).

    Returns:
        float:
            The median of the calibration errors across all percentile bins.
            
    Raises:
        ValueError: If y_true and y_pred_proba have different lengths.
    """
    if len(y_true) != len(y_pred_proba):
        raise ValueError("Inputs y_true and y_pred_proba must have the same length.")

    # 1. Create a DataFrame for easier manipulation
    df = pd.DataFrame({
        'y_true': y_true,
        'y_pred_proba': y_pred_proba
    })

    # 2. Create percentile bins based on the predicted probabilities
    # 'pd.qcut' creates bins with an equal number of samples.
    # 'duplicates="drop"' handles cases where bin edges are not unique,
    # which can happen if a model predicts the same probability many times.
    try:
        df['percentile_bin'] = pd.qcut(df['y_pred_proba'], q=n_bins, labels=False, duplicates='drop')
    except ValueError as e:
        # This can happen if there are too few unique probabilities for the number of bins
        print(f"Warning: Could not create {n_bins} bins due to non-unique probabilities. "
              f"Consider using a smaller n_bins. Error: {e}")
        # Fallback to a smaller number of bins
        df['percentile_bin'] = pd.qcut(df['y_pred_proba'], q=10, labels=False, duplicates='drop')


    # 3. For each percentile bin, calculate the mean of y_true and y_pred_proba
    calibration_data = df.groupby('percentile_bin').agg(
        mean_y=('y_true', 'mean'),
        mean_p=('y_pred_proba', 'mean')
    ).reset_index()

    # 4. Calculate the error for each bin
    # e = mean(p) - mean(y)
    calibration_data['error'] = np.abs(calibration_data['mean_p'] - calibration_data['mean_y'])

    # 5. Take the median of the errors as the final metric
    median_error = calibration_data['error'].median()
    total_error = calibration_data['error'].sum()
    mean_error = calibration_data['error'].mean()

    return median_error, total_error, mean_error

def evaluate_model(y_true,y_pred_proba,threshold=0.5):
# --- 5. Evaluate Model Performance: Metrics ---

    print("\n--- Performance Metrics on Test Set ---")
    median_calibration_error_metric,total_calibration_error_metric,mean_calibration_error_metric = median_calibration_error(y_true,y_pred_proba)
    brier_score_loss_metric = brier_score_loss(y_true,y_pred_proba)
    log_loss_metric = log_loss(y_true,y_pred_proba)

    print(f'brier_score_loss: {brier_score_loss_metric}')
    print(f'log_loss: {log_loss_metric}')
    print(f'median_calibration_error_metric: {median_calibration_error_metric}')
    print(f'total_calibration_error_metric: {total_calibration_error_metric}')
    print(f'mean_calibration_error_metric: {mean_calibration_error_metric}')


    threshold = y_true.mean()
    pred_labels = np.where(y_pred_proba>threshold,1,0)

    # Accuracy
    accuracy = accuracy_score(y_true, pred_labels)
    print(f"Accuracy: {accuracy:.4f}")

    # Classification Report (Precision, Recall, F1-Score)
    print("\nClassification Report:")
    print(classification_report(y_true, pred_labels, target_names=['Class 0', 'Class 1']))

    # Confusion Matrix
    cm = confusion_matrix(y_true, pred_labels)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Predicted 0', 'Predicted 1'],
                yticklabels=['Actual 0', 'Actual 1'])
    plt.title('Confusion Matrix')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()

    # ROC Curve and AUC Score
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Chance (AUC = 0.50)')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.show()


    # --- 6. Evaluate Model Performance: Calibration Plots ---

    print("\n--- Assessing Model Calibration ---")

    # 6a. Reliability Diagram (Calibration Curve)
    # This plot shows how well the predicted probabilities match the actual outcomes.
    fraction_of_positives, mean_predicted_value = calibration_curve(y_true, y_pred_proba, n_bins=10)

    plt.figure(figsize=(8, 8))
    plt.plot(mean_predicted_value, fraction_of_positives, "s-", label="Logistic Regression")
    plt.plot([0, 1], [0, 1], "k:", label="Perfectly Calibrated")
    plt.xlabel("Mean Predicted Probability (per bin)")
    plt.ylabel("Fraction of Positives (per bin)")
    plt.title("Calibration Plot (Reliability Diagram)")
    plt.legend()
    plt.show()

    # 6b. Histogram of Predicted Probabilities
    # This shows the distribution of the model's confidence.
    plt.figure(figsize=(10, 6))
    sns.histplot(y_pred_proba, kde=True, bins=30)
    plt.xlabel("Predicted Probability of being Class 1")
    plt.ylabel("Frequency")
    plt.title("Distribution of Predicted Probabilities")
    plt.show()

