function predict() {
    fetch("/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            air_temp: 310,
            process_temp: 320,
            rpm: 1800,
            torque: 50
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("health").innerText = data.health_score;
        document.getElementById("probability").innerText = data.failure_probability + "%";
        document.getElementById("risk").innerText = data.risk_level;
    });
}