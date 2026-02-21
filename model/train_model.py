import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# -------------------------------------------------
# 1️⃣  LOAD DATA (Safe Absolute Path)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "ai4i2020.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully")
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
# 3️⃣  TRAIN-TEST SPLIT (Stratified for imbalance)
# -------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------------------------
# 4️⃣  MODEL TRAINING
# -------------------------------------------------

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nModel Training Completed")

# -------------------------------------------------
# 5️⃣  EVALUATION
# -------------------------------------------------

y_pred = model.predict(X_test)

print("\nTest Accuracy:", model.score(X_test, y_test))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -------------------------------------------------
# 6️⃣  SAVE MODEL
# -------------------------------------------------

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully at:", MODEL_PATH)

# -------------------------------------------------
# 7️⃣  QUICK SANITY TEST
# -------------------------------------------------

sample = [[325, 335, 2100, 65]]
prob = model.predict_proba(sample)[0][1]

print("\nSample Prediction Probability:", round(prob * 100, 2), "%")