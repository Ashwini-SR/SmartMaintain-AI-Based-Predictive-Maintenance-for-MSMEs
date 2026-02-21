import os
from datetime import datetime
import numpy as np
import joblib
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# -------------------------------------------------
# LOAD MODEL
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

model = joblib.load(MODEL_PATH)
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

        if air_temp <= 0 or process_temp <= 0 or rpm <= 0 or torque <= 0:
            return jsonify({"error": "All values must be positive"}), 400

    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid input data"}), 400

    # -----------------------------
    # MODEL PREDICTION
    # -----------------------------
    features = np.array([[air_temp, process_temp, rpm, torque]])

    prediction = model.predict_proba(features)[0][1]
    failure_probability = round(prediction * 100, 2)
    health_score = round(100 - failure_probability)

    # -----------------------------
    # RISK LEVEL
    # -----------------------------
    if failure_probability < 15 :
        risk = "LOW"
    elif failure_probability <30:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    # -----------------------------
    # ROI CALCULATION (Expected Loss)
    # -----------------------------
    breakdown_cost = 50000
    failures_per_month = 3

    probability_decimal = failure_probability / 100
    expected_monthly_loss = probability_decimal * breakdown_cost * failures_per_month
    monthly_savings = round(expected_monthly_loss)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -----------------------------
    # SAVE TO DATABASE
    # -----------------------------
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (air_temp, process_temp, rpm, torque,
         failure_probability, health_score,
         risk_level, monthly_savings, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        air_temp,
        process_temp,
        rpm,
        torque,
        failure_probability,
        health_score,
        risk,
        monthly_savings,
        timestamp
    ))

    conn.commit()
    conn.close()

    # -----------------------------
    # RETURN RESPONSE
    # -----------------------------
    return jsonify({
        "failure_probability": failure_probability,
        "health_score": health_score,
        "risk_level": risk,
        "monthly_savings": monthly_savings,
        "timestamp": timestamp
    })


@app.route("/history", methods=["GET"])
def get_history():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT health_score, failure_probability,
               risk_level, monthly_savings, timestamp
        FROM predictions
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    history_data = [
        {
            "health_score": row[0],
            "failure_probability": row[1],
            "risk_level": row[2],
            "monthly_savings": row[3],
            "timestamp": row[4]
        }
        for row in rows
    ]

    return jsonify(history_data)


# -------------------------------------------------
# RUN
# -------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False)