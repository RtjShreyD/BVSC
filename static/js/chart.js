document.addEventListener("DOMContentLoaded", function () {
    var ctx = document.getElementById("callsChart").getContext("2d");

    // Flask passes data as JSON, parse it properly
    var labels = JSON.parse(document.getElementById("chart-data").getAttribute("data-labels"));
    var callCounts = JSON.parse(document.getElementById("chart-data").getAttribute("data-callcounts"));
    var totalCosts = JSON.parse(document.getElementById("chart-data").getAttribute("data-totalcosts"));

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Number of Calls",
                    data: callCounts,
                    backgroundColor: "rgba(54, 162, 235, 0.5)",
                    borderColor: "rgba(54, 162, 235, 1)",
                    borderWidth: 1
                },
                {
                    label: "Total Cost",
                    data: totalCosts,
                    backgroundColor: "rgba(255, 99, 132, 0.5)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
