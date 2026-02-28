console.log("JS Loaded");

let vibChart;
let tempChart;

// --------------------------------------
// INITIALIZE AFTER PAGE LOAD
// --------------------------------------
window.onload = function () {

    const ctx1 = document.getElementById("tempChart").getContext("2d");
    tempChart = new Chart(ctx1, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Health Score %", data: [], borderWidth: 2, tension: 0.3 }] },
        options: { responsive: true, scales: { y: { min: 0, max: 100 } } }
    });

    const ctx2 = document.getElementById("vibChart").getContext("2d");
    vibChart = new Chart(ctx2, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Failure Probability %", data: [], borderWidth: 2, tension: 0.3 }] },
        options: { responsive: true, scales: { y: { min: 0, max: 100 } } }
    });

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

        document.getElementById("health-score").innerText = result.health_score + "%";
        document.getElementById("failure-prob").innerText = result.failure_probability + "%";
        document.getElementById("risk-level").innerText = result.risk_level;
        document.getElementById("confidence-score").innerText = result.confidence_score + "%";

        document.getElementById("display-breakdown-cost").innerText = data.breakdown_cost.toLocaleString();
        document.getElementById("display-downtime").innerText = "10 Hours";
        document.getElementById("display-failures").innerText = data.failures_per_month;
        document.getElementById("final-savings").innerText = result.monthly_savings.toLocaleString();

        const riskElement = document.getElementById("risk-level");
        riskElement.style.color =
            result.risk_level === "HIGH" ? "red" :
            result.risk_level === "MEDIUM" ? "orange" : "green";

        const alertBox = document.getElementById("alert-list");
        alertBox.innerHTML =
            result.risk_level === "HIGH" ? "<li style='color:red;'>⚠ Immediate maintenance required!</li>" :
            result.risk_level === "MEDIUM" ? "<li style='color:orange;'>⚠ Monitor machine closely.</li>" :
            "<li style='color:green;'>Machine running normally.</li>";

        const shapBox = document.getElementById("shap-explanation");
        if (shapBox && result.recommendation_detail) {
            shapBox.innerHTML = "";
            result.recommendation_detail.forEach(sentence => {
                let color = sentence.includes("increasing") ? "red" : "green";
                shapBox.innerHTML += `<li style="color:${color};">${sentence}</li>`;
            });
        }

        const shapList = document.getElementById("shap-details");
        if (shapList && result.shap_explanation) {
            shapList.innerHTML = "";
            Object.entries(result.shap_explanation).forEach(([key, value]) => {
                let color = value > 0 ? "red" : "green";
                shapList.innerHTML += `<li style="color:${color};">${key}: ${value}</li>`;
            });
        }

        const summaryBox = document.getElementById("executive-summary");
        if (summaryBox) {
            summaryBox.innerText =
                `This machine is currently classified as ${result.risk_level} risk. Immediate action on ${result.top_risk_factor} is recommended.`;
        }

        const topRiskBox = document.getElementById("top-risk");
        if (topRiskBox) {
            topRiskBox.innerText = `${result.top_risk_factor} (Impact: ${result.top_impact_value})`;
        }

        loadHistory();
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Prediction failed. Check server.");
    });
}


// --------------------------------------
// LOAD HISTORY FOR CHARTS
// --------------------------------------
function loadHistory() {

    fetch("/history?order=DESC&page=1&limit=20")
        .then(res => res.json())
        .then(data => {

            if (!Array.isArray(data) || data.length === 0) return;

            data.reverse();

            tempChart.data.labels = [];
            tempChart.data.datasets[0].data = [];

            vibChart.data.labels = [];
            vibChart.data.datasets[0].data = [];

            data.forEach(item => {
                tempChart.data.labels.push(item.timestamp);
                tempChart.data.datasets[0].data.push(item.health_score);

                vibChart.data.labels.push(item.timestamp);
                vibChart.data.datasets[0].data.push(item.failure_probability);
            });

            tempChart.update();
            vibChart.update();
        })
        .catch(err => console.error("History fetch failed:", err));
}


// --------------------------------------
// RESET DASHBOARD
// --------------------------------------
function resetDashboard() {
    document.getElementById("health-score").innerText = "--";
    document.getElementById("failure-prob").innerText = "--";
    document.getElementById("risk-level").innerText = "--";
    document.getElementById("savings").innerText = "₹0";
}
// --------------------------------------
// DOWNLOAD REPORT (PDF)
// --------------------------------------
function getChartImage(chart) {
    return chart.toBase64Image();
}

function downloadReport() {

    const data = {
        machine_id: document.getElementById("machine_id").value,
        failure_probability: document.getElementById("failure-prob").innerText.replace("%",""),
        health_score: document.getElementById("health-score").innerText.replace("%",""),
        risk_level: document.getElementById("risk-level").innerText,
        monthly_savings: document.getElementById("final-savings").innerText,
        confidence_score: document.getElementById("confidence-score").innerText.replace("%",""),

        // NEW IMPORTANT PART
        health_chart: getChartImage(tempChart),
        failure_chart: getChartImage(vibChart)
    };

    fetch("/download-report", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "SmartMaintain_AI_Report.pdf";
        a.click();
    });
}