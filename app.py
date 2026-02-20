from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# ----------------------------
# ROUTES FOR FRONTEND PAGES
# ----------------------------

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        file = request.files["file"]
        df = pd.read_csv(file)

        # TEMPORARY dummy values (until model is ready)
        probability = 25
        health_score = 75
        risk = "LOW"

        return render_template(
            "predict.html",
            prediction=True,
            probability=probability,
            health_score=health_score,
            risk=risk
        )

    return render_template("predict.html")


@app.route("/cost")
def cost():
    # Dummy values for now
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
# RUN THE APP
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)