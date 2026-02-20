// Temperature Chart
const tempCtx = document.getElementById('tempChart')?.getContext('2d');
if (tempCtx) {
    new Chart(tempCtx, {
        type: 'line',
        data: {
            labels: ['1pm', '2pm', '3pm', '4pm', '5pm', '6pm'],
            datasets: [{
                label: 'Temperature',
                data: [60, 62, 65, 66, 64, 63],
                borderWidth: 2
            }]
        }
    });
}

// Vibration Chart
const vibCtx = document.getElementById('vibChart')?.getContext('2d');
if (vibCtx) {
    new Chart(vibCtx, {
        type: 'line',
        data: {
            labels: ['1pm', '2pm', '3pm', '4pm', '5pm', '6pm'],
            datasets: [{
                label: 'Vibration',
                data: [5, 7, 6, 8, 7, 6],
                borderWidth: 2
            }]
        }
    });
}