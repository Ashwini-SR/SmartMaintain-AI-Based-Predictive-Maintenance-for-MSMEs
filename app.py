import os
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
from flask import Flask, render_template, request, jsonify
import sqlite3
import shap

app = Flask(__name__)

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

model = joblib.load(MODEL_PATH)
explainer = shap.TreeExplainer(model)

print("Model loaded successfully.")

# -------------------------------------------------
# INITIALIZE DATABASE
# -------------------------------------------------
def init_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_id TEXT,
            air_temp REAL,
            process_temp REAL,
            rpm REAL,
            torque REAL,
            failure_probability REAL,
            health_score REAL,
            risk_level TEXT,
            monthly_savings REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# -------------------------------------------------
# ROUTES
# -------------------------------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # -----------------------------
    # INPUT VALIDATION
    # -----------------------------
    try:
        air_temp = float(data["air_temp"])
        process_temp = float(data["process_temp"])
        rpm = float(data["rpm"])
        torque = float(data["torque"])
        machine_id = data.get("machine_id", "Machine-1")

        if not (250 <= air_temp <= 400):
           return jsonify({"error": "Air temperature out of realistic range"}), 400

        if not (250 <= process_temp <= 500):
           return jsonify({"error": "Process temperature out of realistic range"}), 400

        if not (500 <= rpm <= 5000):
            return jsonify({"error": "RPM out of realistic range"}), 400

        if not (1 <= torque <= 1000):
            return jsonify({"error": "Torque out of realistic range"}), 400
            

    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400

    # -----------------------------
    # CREATE FEATURE DF
    # -----------------------------
    X_df = pd.DataFrame(
    [[air_temp, process_temp, rpm, torque]],
    columns=model.feature_names_in_
)
    # -----------------------------
    # MODEL PREDICTION
    # -----------------------------
    prediction = model.predict_proba(X_df)[0][1]
    failure_probability = round(prediction * 100, 2)
    health_score = round(100 - failure_probability, 2)

    # -----------------------------
    # SHAP EXPLANATION
    # -----------------------------
    shap_values = explainer.shap_values(X_df)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
        
    shap_array = np.array(shap_values)
    

    shap_dict = {}
    for i, feature in enumerate(model.feature_names_in_):
        shap_dict[feature] = round(float(shap_values[0][i]), 4)

    # Identify top risk factor
    top_feature = max(shap_dict, key=lambda k: abs(shap_dict[k]))
    top_impact = shap_dict[top_feature]

    # Human readable SHAP explanation
    recommendation_detail = []
    for feature, value in shap_dict.items():
        if value > 0:
            recommendation_detail.append(
                f"{feature} is increasing failure probability."
            )
        else:
            recommendation_detail.append(
                f"{feature} is stabilizing machine condition."
            )

    # -----------------------------
    # RISK LEVEL
    # -----------------------------
    if failure_probability < 15:
        risk = "LOW"
    elif failure_probability < 30:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # -----------------------------
    # ROI CALCULATION
    # -----------------------------
    breakdown_cost = float(data.get("breakdown_cost", 50000))
    failures_per_month = float(data.get("failures_per_month", 3))

    probability_decimal = failure_probability / 100
    expected_monthly_loss = probability_decimal * breakdown_cost * failures_per_month
    monthly_savings = round(expected_monthly_loss, 2)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -----------------------------
    # SAVE TO DATABASE
    # -----------------------------
    DB_PATH = os.path.join(BASE_DIR, "history.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (machine_id, air_temp, process_temp, rpm, torque,
         failure_probability, health_score,
         risk_level, monthly_savings, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        machine_id, air_temp, process_temp, rpm, torque,
        failure_probability, health_score, risk,
        monthly_savings, timestamp
    ))

    conn.commit()
    conn.close()

    # -----------------------------
    # RETURN RESPONSE
    # -----------------------------
    return jsonify({
        "machine_id": machine_id,
        "failure_probability": failure_probability,
        "health_score": health_score,
        "risk_level": risk,
        "monthly_savings": monthly_savings,
        "timestamp": timestamp,
        "shap_explanation": shap_dict,
        "recommendation_detail": recommendation_detail,
        "top_risk_factor": top_feature,
        "top_impact_value": top_impact
    })


@app.route("/history", methods=["GET"])
def get_history():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT machine_id, health_score,
               failure_probability, risk_level,
               monthly_savings, timestamp
        FROM predictions
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    history_data = [
        {
            "machine_id": row[0],
            "health_score": row[1],
            "failure_probability": row[2],
            "risk_level": row[3],
            "monthly_savings": row[4],
            "timestamp": row[5]
        }
        for row in rows
    ]

    return jsonify(history_data)


# -------------------------------------------------
# RUN
# -------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False)