 SmartMaintain – AI-Based Predictive Maintenance for MSMEs

---

1) Problem Statement

Unplanned equipment failures in MSMEs (Micro, Small & Medium Enterprises) cause:

* Unexpected downtime
* High emergency repair costs
* Production delays
* Reduced equipment lifespan

Most MSMEs rely on reactive maintenance instead of predictive intelligence due to:

* High cost of industrial IoT systems
* Lack of data science expertise
* No affordable AI-based solution

**Objective:**
Build a low-cost, AI-driven predictive maintenance system that estimates machine failure probability and provides risk classification for proactive decision-making.

---

2) Proposed Solution

SmartMaintain is a lightweight web-based predictive maintenance system that:

* Accepts machine sensor data (CSV upload)
* Predicts failure probability using ML model
* Calculates health score
* Classifies risk level (Low / Medium / High)
* Estimates cost savings from preventive action

Designed specifically for MSMEs with minimal technical overhead.

---

3) Architecture Diagram (Text Version)

You can later convert this into a visual diagram.

```
Machine Sensor Data (CSV)
        ↓
Flask Backend (app.py)
        ↓
Load Trained ML Model (model.pkl)
        ↓
Failure Probability Prediction
        ↓
Risk Classification + Health Score
        ↓
Frontend Dashboard Display
```

If you want stronger impact, create diagram using:

* Draw.io
* Canva
* Lucidchart

---

4) Tech Stack

### Backend

* Python
* Flask
* Pandas
* Scikit-learn
* Joblib

### Frontend

* HTML
* CSS
* JavaScript

### ML Model

* Classification model (predict_proba)
* Trained using industrial equipment dataset

### Version Control

* Git
* GitHub

---

5) Project Structure

```
smartmaintain/
│
├── app.py
├── requirements.txt
│
├── model/
│   ├── train_model.py
│   └── model.pkl
│
├── data/
│   └── dataset.csv
│
├── templates/
│   ├── dashboard.html
│   ├── predict.html
│   └── cost.html
│
└── static/
    ├── style.css
    └── script.js
```

---

6) How to Run Locally

### Step 1 — Clone Repository

```bash
git clone <your-repo-link>
cd smartmaintain
```

### Step 2 — Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Train Model (If model.pkl not present)

```bash
python model/train_model.py
```

### Step 5 — Run Application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

7) Features

* CSV-based industrial sensor upload
* Real-time failure probability prediction
* Risk classification
* Machine health score
* ROI and cost-saving estimation module
* Defensive error handling for production safety

---

8) Innovation Aspect (Important for Judges)

Unlike high-cost industrial IoT systems:

* Designed specifically for MSMEs
* Minimal hardware dependency
* Simple CSV ingestion model
* Lightweight deployment
* Easily integrable with existing ERP systems

---

 9) Future Scope

* Real-time IoT sensor integration
* Dashboard analytics charts
* Model retraining pipeline
* Cloud deployment
* SMS/Email alert system
* Feature importance visualization
