// chart1
const ctx1 = document.getElementById('myChart1');

const config1 = {
    type: 'bar',
    data: {
        //labels: [],
        datasets: [{
            label: 'vote',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(255, 205, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(92, 234, 116, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(92, 234, 116)',
                'rgb(153, 102, 255)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: true,
        maintainAspectRatio: false,
    },
};

fetch('/get_top_places')
    .then(response => response.json())
    .then(apiData => {
        config1.data.labels = apiData.labels;
        config1.data.datasets[0].data = apiData.numbers;
        const myChart1 = new Chart(ctx1, config1);
    })
    .catch(error => {
        console.error('Error fetching top places: ', error);
    });

// chart2
const ctx2 = document.getElementById('myChart2');

const config2 = {
    type: 'pie',
    data: {
        datasets: [{
            label: 'percentage',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(255, 205, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(92, 234, 116, 0.7)',
                'rgba(153, 102, 255, 0.7)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(92, 234, 116)',
                'rgb(153, 102, 255)'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false
    }
};

fetch('/get_top_countries')
    .then(response => response.json())
    .then(apiData => {
        config2.data.labels = apiData.labels;
        config2.data.datasets[0].data = apiData.numbers;
        const myChart2 = new Chart(ctx2, config2);
    })
    .catch(error => {
        console.error('Error fetching top countries: ', error);
    });

