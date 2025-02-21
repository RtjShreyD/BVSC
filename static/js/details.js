document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".toggle-details").forEach(anchor => {
        anchor.addEventListener("click", function (event) {
            event.preventDefault();
            
            let year = this.getAttribute("data-year");
            let month = this.getAttribute("data-month");
            let detailsContainer = document.getElementById("details-container");
            let contentDiv = document.getElementById("details-content");

            // Update UI: Show container & loading text
            detailsContainer.style.display = "block";
            contentDiv.innerHTML = "<p>Loading details...</p>";

            // Fetch data from API
            fetch(`/details/${year}/${month}`)
                .then(response => response.text())
                .then(data => {
                    contentDiv.innerHTML = data;
                })
                .catch(error => {
                    contentDiv.innerHTML = "<p>Error loading details</p>";
                });
        });
    });
});
