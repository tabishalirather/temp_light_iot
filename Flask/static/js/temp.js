$(document).ready(function(){
    // Fetch and display the latest temperature data
    $('#btnRefreshTemp').click(function(){
        fetchTemperatureData();
    });

    function fetchTemperatureData() {
        $.getJSON('/get-temperature-data', function(data) {
            var tableContent = '<table class="data-table"><tr><th>DateTime</th><th>Temperature Value</th></tr>';
            data.forEach(function(item){
                var timestamp = (item[0]).toLocaleString();
                tableContent += `<tr><td>${timestamp}</td><td>${item[1]}</td></tr>`;
            });
            $('#temperatureDataDisplay').html(tableContent);
        }).fail(function() {
            console.log("Error fetching temperature data");
        });
    }

    // Initial fetch on page load
    fetchTemperatureData();
});
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('hourlyTemperatureChart').getContext('2d');
    
    fetch('/hourly-temperature-data')
        .then(response => response.json())
        .then(data => {
            console.log("Data:", data);

            const timestamps = data.map(item => item.timestamp);
            const lightValues = data.map(item => item.temperature);

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: timestamps,
                    datasets: [{
                        label: 'Hourly Temprature Data',
                        data: lightValues,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        fill: true,
                        tension: 0.1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            title: {
                                display: true,
                                text: 'Temperature (C)'
                            },
                        min: 0,
                        max: 60,
                        },
                        
                        x: {
                            title: {
                                display: true,
                                text: 'Timestamp'
                            }
                        }
                    },
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top',
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                        },
                    },
                    interaction: {
                        mode: 'nearest',
                        axis: 'x',
                        intersect: false
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error fetching hourly light data:', error);
        });
});
