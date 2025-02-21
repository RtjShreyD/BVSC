# Call Statistics Dashboard

## Overview
This project is a **Call Statistics Dashboard** that visualizes monthly call trends and displays detailed call records for each month. It includes interactive charts, a paginated data table, and collapsible details sections for in-depth analysis. The dashboard is built using Flask for the backend and JavaScript (with Chart.js) for frontend data visualization.

## Tech Stack
- **Backend:** Flask (Python)
- **Frontend:** HTML, Bootstrap, JavaScript (Chart.js, Fetch API)
- **Database:** SQLite (or any other database with minor modifications)
- **Templating Engine:** Jinja2

## Features
- **Monthly Call Trends Chart**: Visualizes the number of calls and total cost.
- **Paginated Data Table**: Displays call statistics per month.
- **Collapsible Details Section**: Fetches and displays detailed call records dynamically.
- **AJAX-based Pagination**: Prevents page reload when navigating through paginated call records.
- **Mobile Responsive**: Designed with Bootstrap for better usability on all screen sizes.

## File Structure
```
├── main.py                 # Flask application entry point
├── notes.md                # Additional project notes
├── static
│   ├── css
│   │   └── styles.css      # Custom CSS styles
│   └── js
│       ├── chart.js       # JavaScript for Chart.js visualization
│       └── details.js     # JavaScript for handling AJAX and pagination
└── templates
    ├── base.html           # Base layout template
    ├── dashboard.html      # Main dashboard page
    └── details.html        # AJAX-loaded call details
```

## Setup and Running the Project
### Prerequisites
- Python 3.7+
- Flask (`pip install flask`)
- SQLite (or another database if needed)

### Steps to Run
1. **Clone the Repository**
   ```sh
   git clone https://github.com/rtjshreyd/BVSC.git
   cd call-dashboard
   ```

2. **Install Dependencies**
   ```sh
   pip install flask
   ```

3. **Run the Flask Server**
   ```sh
   python main.py
   ```

4. **Open in Browser**
   Visit `http://127.0.0.1:5000/` to access the dashboard.

## API Endpoints
- **`/`** - Main dashboard
- **`/details/<year>/<month>?page=<num>`** - Fetch paginated call details for a specific month

## Credits
Developed by **Shreyansh Dubey** (Tecelit Development Solutions).

