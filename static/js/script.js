console.log("JS Loaded");

let vibChart;
let tempChart;

// --------------------------------------
// INITIALIZE AFTER PAGE LOAD
// --------------------------------------
window.onload = function () {

    // ------------------------
    // HEALTH SCORE CHART
    // ------------------------
    const ctx1 = document.getElementById("tempChart").getContext("2d");

    tempChart = new Chart(ctx1, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Health Score %",
                data: [],
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { min: 0, max: 100 }
            }
        }
    });

    // ------------------------
    // FAILURE PROBABILITY CHART
    // ------------------------
    const ctx2 = document.getElementById("vibChart").getContext("2d");

    vibChart = new Chart(ctx2, {
        type: "line",
        data: {
            labels: [],
            datasets: [{
                label: "Failure Probability %",
                data: [],
                borderWidth: 2,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { min: 0, max: 100 }
            }
        }
    });
    


    // Load history automatically on page refresh
    loadHistory();
};


// --------------------------------------
// PREDICT FUNCTION
// --------------------------------------
function predict() {

    const data = {
    machine_id: document.getElementById("machine_id").value,
    air_temp: document.getElementById("air_temp").value,
    process_temp: document.getElementById("process_temp").value,
    rpm: document.getElementById("rpm").value,
    torque: document.getElementById("torque").value,
    breakdown_cost: Number(document.getElementById("breakdown_cost").value) || 50000,
    failures_per_month: Number(document.getElementById("failures_per_month").value) || 3
};
    if (!data.air_temp || !data.process_temp || !data.rpm || !data.torque) {
    alert("Please fill all machine parameters.");
    return;
}
    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {

        if (result.error) {
            alert(result.error);
            resetDashboard();
            return;
        }

        // ------------------------
        // UPDATE METRICS
        // ------------------------
        document.getElementById("health-score").innerText =
            result.health_score + "%";

        document.getElementById("failure-prob").innerText =
            result.failure_probability + "%";

        document.getElementById("risk-level").innerText =
            result.risk_level;

        // ------------------------
        // RISK COLOR LOGIC
        // ------------------------
        const riskElement = document.getElementById("risk-level");

        if (result.risk_level === "HIGH") {
            riskElement.style.color = "red";
        } else if (result.risk_level === "MEDIUM") {
            riskElement.style.color = "orange";
        } else {
            riskElement.style.color = "green";
        }

        // ------------------------
        // COST SAVINGS
        // ------------------------
        document.getElementById("savings").innerText =
            "₹" + result.monthly_savings.toLocaleString();

        // ------------------------
        // ALERT BOX
        // ------------------------
        const alertBox = document.getElementById("alert-list");

        if (alertBox) {
            if (result.risk_level === "HIGH") {
                alertBox.innerHTML =
                    "<li style='color:red;'>⚠ Immediate maintenance required!</li>";
            } else if (result.risk_level === "MEDIUM") {
                alertBox.innerHTML =
                    "<li style='color:orange;'>⚠ Monitor machine closely.</li>";
            } else {
                alertBox.innerHTML =
                    "<li style='color:green;'>Machine running normally.</li>";
            }
        }
        // ------------------------
// SHAP EXPLANATION DISPLAY
// ------------------------
const shapBox = document.getElementById("shap-explanation");

if (shapBox && result.shap_explanation) {

    shapBox.innerHTML = "";

    for (const [feature, value] of Object.entries(result.shap_explanation)) {

        const color = value > 0 ? "red" : "green";

        shapBox.innerHTML += `
            <li style="color:${color}">
                ${feature}: ${value}
            </li>
        `;
    }
}
const shapList = document.getElementById("shap-details");

if (shapList && result.shap_explanation) {

    shapList.innerHTML = "";

    Object.entries(result.shap_explanation).forEach(([key, value]) => {

        let color = value > 0 ? "red" : "green";

        shapList.innerHTML +=
            `<li style="color:${color};">
                ${key}: ${value}
             </li>`;
    });
}
        const summaryBox = document.getElementById("executive-summary");

if (summaryBox) {

    let riskText = result.risk_level;
    let driver = result.top_risk_factor || "key parameters";

    summaryBox.innerText =
        "This machine is currently classified as " +
        riskText +
        " risk. Immediate action on " +
        driver +
        " is recommended.";
}
const topRiskBox = document.getElementById("top-risk");

if (topRiskBox && result.top_risk_factor) {
    topRiskBox.innerText =
        result.top_risk_factor +
        " (Impact: " +
        result.top_impact_value +
        ")";
}
result.top_risk_factor

        // Reload charts
        loadHistory();
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Prediction failed. Check server.");
    });
}
// ------------------------
// TOP RISK FACTOR DISPLAY
// ------------------------


// --------------------------------------
// LOAD HISTORY + UPDATE BOTH GRAPHS
// --------------------------------------
async function loadHistory() {

    try {
        const response = await fetch("/history");
        const data = await response.json();

        const healthData = data.map(item => item.health_score);
        const failureData = data.map(item => item.failure_probability);

        const labels = data.map(item =>
    item.machine_id + " (" + item.timestamp + ")"
);

        if (tempChart) {
            tempChart.data.labels = labels;
            tempChart.data.datasets[0].data = healthData;
            tempChart.update();
        }

        if (vibChart) {
            vibChart.data.labels = labels;
            vibChart.data.datasets[0].data = failureData;
            vibChart.update();
        }
        

// ------------------------
// HISTORY LIST UPDATE
// ------------------------
const historyList = document.getElementById("history-list");

if (historyList) {

    historyList.innerHTML = "";

    data.forEach(item => {

        historyList.innerHTML += `
            <li>
                <strong>${item.machine_id}</strong> |
                Risk: ${item.risk_level} |
                Health: ${item.health_score}% |
                Savings: ₹${item.monthly_savings}
            </li>
        `;
    });
}

    } catch (error) {
        console.error("History load failed:", error);
    }
}


// --------------------------------------
// RESET DASHBOARD ON ERROR
// --------------------------------------
function resetDashboard() {
    document.getElementById("health-score").innerText = "--";
    document.getElementById("failure-prob").innerText = "--";
    document.getElementById("risk-level").innerText = "--";
    document.getElementById("savings").innerText = "₹0";
}