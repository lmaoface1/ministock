import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, f1_score

from features import build_features
from labels import add_labels

FEATURE_COLUMNS = [
    "days_since_last_sale",
    "total_sold_30d",
    "total_sold_90d",
    "capital_tied",
    "turnover_rate",
]


def main():
    df = build_features()
    df = add_labels(df)

    X = df[FEATURE_COLUMNS]
    y = df["is_frozen"]

    print("Class distribution:")
    print(y.value_counts())
    print()

    # NOTE: with only 8 rows, stratified split needs at least 2 of each class
    # in both train and test - this is expected to be tiny for practice purposes
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("=== Test set evaluation ===")
    print(classification_report(y_test, y_pred, zero_division=0))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Cross-validation on full data (small dataset, so folds are small too)
    cv_scores = cross_val_score(model, X, y, cv=3, scoring="f1_macro")
    print(f"\nCV macro-F1 scores: {cv_scores}")
    print(f"Mean CV macro-F1: {cv_scores.mean():.3f}")

    # Save the model
    os.makedirs("artifacts", exist_ok=True)
    joblib.dump(model, "artifacts/frozen_classifier.pkl")
    print("\nModel saved to artifacts/frozen_classifier.pkl")


if __name__ == "__main__":
    main()