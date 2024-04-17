$(document).ready(function(){
    $('#btnRefresh').click(function(){
        $.getJSON('/get-light-data', function(data){
    var tableContent = `<table class="data-table">
                                    <tr>
                                        <th>DateTime</th>
                                        <th>Light Value</th>
                                    </tr>`;
    data.forEach(function(item){
        // Parse the timestamp string into a JavaScript Date object
        var timestamp = item[0];


        // Construct the formatted date string in "dd/mm/yy hh:mm:ss" format

        // Append the formatted date and light value to the table content
        tableContent += `<tr>
                            <td>${timestamp}</td>
                            <td>${item[1]}</td>
                        </tr>`;
    });
    
    $('#dataDisplay').html(tableContent);
});

    $('#btnControlLED').click(function(){
        var ledState = $('#ledState').val();
        $.post('/control-led', { led_state: ledState }, function(response){
            alert(response.message);
        });
    });
});

});
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('hourlyLightChart').getContext('2d');
    
    fetch('/hourly-light-data')
        .then(response => response.json())
        .then(data => {
            console.log("Data:", data);

            const timestamps = data.map(item => item.timestamp);
            const lightValues = data.map(item => item.light_value);

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: timestamps,
                    datasets: [{
                        label: 'Hourly Light Intensity',
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
                                text: 'Light Intensity (lux)'
                            }
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
