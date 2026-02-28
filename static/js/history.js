let currentPage = 1;
const limit = 10;
let currentOrder = "DESC";

function buildQueryParams() {
    const machine = document.getElementById("search-machine").value;
    const risk = document.getElementById("search-risk").value;
    const date = document.getElementById("search-date").value;

    let params = `?order=${currentOrder}&page=${currentPage}&limit=${limit}`;
    if (machine) params += `&machine=${machine}`;
    if (risk) params += `&risk=${risk}`;
    if (date) params += `&date=${date}`;

    return params;
}

function loadHistory() {
    fetch("/history" + buildQueryParams())
        .then(res => res.json())
        .then(data => {
            const tableBody = document.querySelector("#history-table tbody");
            tableBody.innerHTML = "";

            data.forEach(item => {

                let riskClass =
                    item.risk_level === "HIGH" ? "risk-high" :
                    item.risk_level === "MEDIUM" ? "risk-medium" :
                    "risk-low";

                tableBody.innerHTML += `
                    <tr>
                        <td>${item.machine_id}</td>
                        <td>${item.health_score}%</td>
                        <td>${item.failure_probability}%</td>
                        <td><span class="${riskClass}">${item.risk_level}</span></td>
                        <td>₹${item.monthly_savings}</td>
                        <td>${item.timestamp}</td>
                    </tr>
                `;
            });

            document.getElementById("current-page").innerText = currentPage;
        });
}

// ----------------------------
// EVENT LISTENERS
// ----------------------------
document.addEventListener("DOMContentLoaded", loadHistory);

document.getElementById("sort-asc").addEventListener("click", () => {
    currentOrder = "ASC";
    currentPage = 1;
    loadHistory();
});

document.getElementById("sort-desc").addEventListener("click", () => {
    currentOrder = "DESC";
    currentPage = 1;
    loadHistory();
});

document.getElementById("prev-page").addEventListener("click", () => {
    if (currentPage > 1) {
        currentPage--;
        loadHistory();
    }
});

document.getElementById("next-page").addEventListener("click", () => {
    currentPage++;
    loadHistory();
});

document.getElementById("search-btn").addEventListener("click", () => {
    currentPage = 1;
    loadHistory();
});

// Export CSV
document.getElementById("export-csv").addEventListener("click", () => {
    fetch("/history?order=DESC&export=csv")
        .then(res => res.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "prediction_history.csv";
            document.body.appendChild(a);
            a.click();
            a.remove();
        });
});