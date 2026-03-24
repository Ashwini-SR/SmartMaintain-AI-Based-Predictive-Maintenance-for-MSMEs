# SmartMaintain – AI-Based Predictive Maintenance for MSMEs

## 1) Problem Statement

Unplanned equipment failures in MSMEs (Micro, Small & Medium Enterprises) lead to:

- Unexpected downtime
- High emergency repair costs
- Production delays
- Reduced equipment lifespan

Most MSMEs rely on reactive maintenance due to:

- High cost of industrial IoT solutions
- Lack of AI/ML expertise
- Absence of simple predictive tools

**Objective:** Build a low-cost, ML-driven predictive maintenance system that estimates machine failure probability and enables proactive decision-making.

---

## 2) Proposed Solution

SmartMaintain is a lightweight web-based system that:

- Accepts machine parameters (temperature, RPM, torque)
- Predicts failure probability using ML
- Calculates machine health score
- Classifies risk level (Low / Medium / High)
- Estimates cost savings from preventive action
- Stores prediction history for trend analysis

**Live Application:**  
https://smartmaintain-ai-based-predictive.onrender.com

---

## 3) Machine Learning Approach

### Models Explored

- Linear Regression (baseline understanding)
- Decision Tree (interpretable model)
- Random Forest (final model)

### Final Model

**RandomForestClassifier**

### Reasons:

- Captures nonlinear relationships in sensor data
- Robust to noise
- Works well with imbalanced datasets
- Provides probability outputs (`predict_proba`)

### Handling Class Imbalance:

```python
class_weight = "balanced"
```

---

## 4) Dataset Explanation

**Dataset:** AI4I 2020 Predictive Maintenance Dataset

### Characteristics:

- 10,000 records
- 14 features
- Simulated industrial machine sensor data

### Features Used:

- Air Temperature (K)
- Process Temperature (K)
- Rotational Speed (RPM)
- Torque (Nm)

### Target:

- Machine Failure (0 / 1)

### Class Distribution:

- Normal: 9661
- Failure: 339

This strong imbalance influences model behavior and probability calibration.

---

## 5) Model Performance

- **Accuracy:** 98.1%

### Confusion Matrix:

```python
[[1926   6]
 [  32  36]]
```

### Classification Report (Failure class):

- Precision: 0.86
- Recall: 0.53

---

## 6) Recall Justification and Threshold Strategy

The dataset is highly imbalanced (only 3.4% failures).

### Observations:

- Model is conservative in predicting failures
- Increasing recall would increase false positives

### Trade-off:

- High precision (0.86) → avoids unnecessary maintenance
- Moderate recall (0.53) → some failures may be missed

### Strategy:

Instead of hard classification:

- Use probability scores (`predict_proba`)
- Assign risk levels using thresholds

### Threshold Logic:

- 0–15% → Low
- 15–30% → Medium
- >30% → High

### Justification:

Even a 30% probability is considered high risk due to rarity of failures.

### Benefits:

- Flexible threshold tuning
- Better operational decision-making
- Balanced false positives vs false negatives

---

## 7) Feature Importance (Model Explainability)

Key influencing features:

- Torque (highest impact)
- Rotational Speed
- Process Temperature
- Air Temperature

### Interpretation:

- Higher torque and RPM increase mechanical stress
- Temperature differences indicate abnormal operating conditions
- Combined effect leads to higher failure probability

---

## 8) Output and Results

System outputs:

- Failure Probability (%)
- Health Score (%)
- Risk Level (Low / Medium / High)
- Estimated Monthly Cost Savings

### Example:

- Failure Probability: 26.5%
- Health Score: 73%
- Risk Level: Medium

---

## 9) Visualization and UI

### Dashboard Includes:

- Health Score display
- Failure Probability display
- Risk level indicator with color coding

### Charts (Chart.js):

- Health Score over time
- Failure Probability over time

### Additional Features:

- Alert system based on risk level
- Prediction history tracking

---

## 10) API Documentation

### Endpoint: `POST /predict`

#### Request:

```json
{
  "air_temp": 325,
  "process_temp": 335,
  "rpm": 2100,
  "torque": 65
}
```

#### Response:

```json
{
  "failure_probability": 26.5,
  "health_score": 73,
  "risk_level": "MEDIUM",
  "monthly_savings": 45000,
  "timestamp": "2026-03-24 22:30:00"
}
```

---

### Endpoint: `GET /history`

#### Response:

Returns list of past predictions including:

- health_score
- failure_probability
- risk_level
- timestamp

---

## 11) Architecture

```
Input Parameters
        ↓
Flask Backend (app.py)
        ↓
Load ML Model (model.pkl)
        ↓
Predict Failure Probability
        ↓
Apply Threshold Logic
        ↓
Generate Risk + Health Score + Savings
        ↓
Store in Database (SQLite)
        ↓
Frontend Dashboard Visualization
```

---

## 12) Tech Stack

### Backend:

- Python
- Flask
- Pandas
- Scikit-learn
- Joblib
- SQLite

### Frontend:

- HTML
- CSS
- JavaScript
- Chart.js

### Version Control:

- Git
- GitHub

---

## 13) Project Structure

```
smartmaintain/

├── app.py
├── requirements.txt

├── model/
│   ├── train_model.py
│   └── model.pkl

├── data/
│   └── dataset.csv

├── templates/
│   ├── dashboard.html
│   ├── predict.html
│   └── cost.html

└── static/
    ├── css/style.css
    └── js/script.js
```

---

## 14) How to Run Locally

```bash
git clone <repo-link>
cd smartmaintain

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python model/train_model.py

python app.py
```

Open: http://127.0.0.1:5000

---

## 15) Features

- Real-time failure prediction
- Risk classification
- Health scoring system
- Cost-saving estimation
- Historical tracking with database
- Chart-based visualization
- Input validation and error handling

---

## 16) Innovation (Improved)

| Aspect | Traditional Systems | SmartMaintain |
|------|------------------|--------------|
| Cost | High (IoT hardware required) | Low (software-only) |
| Setup | Complex | Simple |
| Data Source | Real-time sensors | Manual / CSV input |
| Accessibility | Large industries | MSMEs |
| Deployment | Heavy infrastructure | Lightweight web app |

### Key Innovation:

- Eliminates need for expensive IoT setup
- Uses minimal input features for prediction
- Converts ML output into actionable business insights
- Integrates prediction + cost savings + visualization

---

## 17) Future Scope

- IoT sensor integration
- Automated retraining pipeline
- Advanced analytics dashboard
- Alert system (Email/SMS)
- Feature importance visualization in UI
- Cloud scaling
