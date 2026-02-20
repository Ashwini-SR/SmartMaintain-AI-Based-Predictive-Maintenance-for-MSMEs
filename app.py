from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load trained model
model = joblib.load("model/model.pkl")


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[ 
        data["air_temp"],
        data["process_temp"],
        data["rpm"],
        data["torque"]
    ]])

    prediction = model.predict_proba(features)[0][1]
    health_score = int((1 - prediction) * 100)

    if prediction < 0.3:
        risk = "Low"
    elif prediction < 0.7:
        risk = "Medium"
    else:
        risk = "High"

    return jsonify({
        "failure_probability": round(prediction * 100, 2),
        "health_score": health_score,
        "risk_level": risk
    })


@app.route("/cost")
def cost():
    before_cost = 50000
    after_cost = 15000
    hours_saved = 12
    money_saved = before_cost - after_cost
    roi = int((money_saved / after_cost) * 100)

    return render_template(
        "cost.html",
        before_cost=before_cost,
        after_cost=after_cost,
        hours_saved=hours_saved,
        money_saved=money_saved,
        roi=roi
    )


# ----------------------------
# RUN APP
# ----------------------------

if __name__ == "__main__":
    print("Starting SmartMaintain server...")
    app.run(debug=True)