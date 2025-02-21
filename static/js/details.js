document.addEventListener("DOMContentLoaded", function () {
    let currentPage = 1;
    let totalPages = 1;
    let currentYear, currentMonth;

    function fetchDetails(year, month, page = 1) {
        let detailsContainer = document.getElementById("details-container");
        let contentDiv = document.getElementById("details-content");
        let paginationControls = document.getElementById("pagination-controls");

        // Show loading state
        detailsContainer.style.display = "block";
        contentDiv.innerHTML = "<p>Loading details...</p>";
        paginationControls.style.display = "none";  // Hide pagination initially

        // Fetch paginated data
        fetch(`/details/${year}/${month}?page=${page}`)
            .then(response => response.json())
            .then(data => {
                contentDiv.innerHTML = data.html;
                currentPage = data.current_page;
                totalPages = data.total_pages;

                // Update pagination info
                document.getElementById("page-info").textContent = `Page ${currentPage} of ${totalPages}`;
                paginationControls.style.display = totalPages > 1 ? "block" : "none"; 

                // Enable/Disable buttons
                document.getElementById("prev-page").style.visibility = (currentPage > 1) ? "visible" : "hidden";
                document.getElementById("next-page").style.visibility = (currentPage < totalPages) ? "visible" : "hidden";
            })
            .catch(error => {
                contentDiv.innerHTML = "<p>Error loading details</p>";
            });
    }

    document.querySelectorAll(".toggle-details").forEach(anchor => {
        anchor.addEventListener("click", function (event) {
            event.preventDefault();
            currentYear = this.getAttribute("data-year");
            currentMonth = this.getAttribute("data-month");
            fetchDetails(currentYear, currentMonth, 1);
        });
    });

    document.getElementById("prev-page").addEventListener("click", function (event) {
        event.preventDefault();
        if (currentPage > 1) fetchDetails(currentYear, currentMonth, currentPage - 1);
    });

    document.getElementById("next-page").addEventListener("click", function (event) {
        event.preventDefault();
        if (currentPage < totalPages) fetchDetails(currentYear, currentMonth, currentPage + 1);
    });
});
