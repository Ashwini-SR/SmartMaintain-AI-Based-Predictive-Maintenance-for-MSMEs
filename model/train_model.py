import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# -------------------------------------------------
# 1️⃣  LOAD DATA (Absolute-safe path handling)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "ai4i2020.csv")

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)
print("\nClass Distribution:\n", df["Machine failure"].value_counts())

# -------------------------------------------------
# 2️⃣  FEATURE SELECTION
# -------------------------------------------------

X = df[[
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]"
]]

y = df["Machine failure"]

# -------------------------------------------------
# 3️⃣  TRAIN-TEST SPLIT (Stratified)
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# 4️⃣  MODEL TRAINING (Handles imbalance)
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# -------------------------------------------------
# 5️⃣  EVALUATION
# -------------------------------------------------

y_pred = model.predict(X_test)

print("\nTest Accuracy:", model.score(X_test, y_test))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------------------------------
# 6️⃣  SAVE MODEL (inside model folder)
# -------------------------------------------------

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully at:", MODEL_PATH)