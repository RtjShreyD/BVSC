from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
from datetime import datetime
from sqlalchemy import func

load_dotenv()

app = Flask(__name__)

db_url = os.environ.get('MYSQL_URL', 'localhost')
db_user = os.environ.get('MYSQL_USERNAME', None)
db_pass = os.environ.get('MYSQL_PASSWORD', None)
db_name = os.environ.get('MYSQL_DB_NAME', None)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_url}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the BVSCalls Model
class BVSCalls(db.Model):
    __tablename__ = 'BVSCalls'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment primary key
    CallFrom = db.Column(db.String(255), nullable=False)
    CallTo = db.Column(db.String(255), nullable=False)
    CallTime = db.Column(db.DateTime, nullable=False)
    Duration = db.Column(db.Time, nullable=False)
    Billing = db.Column(db.Time, nullable=False)
    Cost = db.Column(db.Float(precision=4), nullable=False, default=0.0000)
    Status = db.Column(db.String(50), nullable=False)


# GET API with Pagination
@app.route('/calls', methods=['GET'])
def get_calls():
    try:
        # Get pagination parameters from request
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        
        # Query the database with pagination
        calls = BVSCalls.query.paginate(page=page, per_page=size, error_out=False)
        
        # Convert results to JSON
        result = [{
            "CallFrom": call.CallFrom,
            "CallTo": call.CallTo,
            "CallTime": call.CallTime.strftime('%Y-%m-%d %H:%M:%S'),
            "Duration": str(call.Duration),
            "Billing": str(call.Billing),
            "Cost": call.Cost,
            "Status": call.Status
        } for call in calls.items]
        
        return jsonify({
            "page": calls.page,
            "size": calls.per_page,
            "total_pages": calls.pages,
            "total_records": calls.total,
            "data": result
        })
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500



@app.route('/dashboard')
def dashboard():
    try:
        current_year = "2018"

        # Query to get call count and total cost per month for the current year
        monthly_data = (
            db.session.query(
                func.MONTH(BVSCalls.CallTime).label("month"),
                func.COUNT(BVSCalls.id).label("call_count"),
                func.SUM(BVSCalls.Cost).label("total_cost")
            )
            .filter(func.YEAR(BVSCalls.CallTime) == current_year)
            .group_by(func.MONTH(BVSCalls.CallTime))
            .order_by(func.MONTH(BVSCalls.CallTime))
            .all()
        )

        # Prepare data for Chart.js
        labels = [str(row.month) for row in monthly_data]
        call_counts = [row.call_count for row in monthly_data]
        total_costs = [row.total_cost or 0 for row in monthly_data]  # Handle None values

        # Prepare data for DataTable
        table_data = [
            {
                "year_month": f"{current_year}-{str(row.month).zfill(2)}", 
                "month": row.month,  # ✅ Add this line
                "call_count": row.call_count, 
                "total_cost": row.total_cost or 0
            }
            for row in monthly_data
        ]

        return render_template(
            "dashboard.html",
            labels=labels,
            call_counts=call_counts,
            total_costs=total_costs,
            table_data=table_data,
            year=current_year
        )

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500

# 🔵 Drill-down View - Extension-wise Breakdown
@app.route('/details/<year>/<month>')
def call_details(year, month):
    try:
        print(year)
        # Fetch call details grouped by extension (CallFrom)
        extension_data = (
            db.session.query(
                BVSCalls.CallFrom.label("extension"),
                func.COUNT(BVSCalls.id).label("call_count"),
                func.SUM(BVSCalls.Cost).label("total_cost")
            )
            .filter(func.YEAR(BVSCalls.CallTime) == year, func.MONTH(BVSCalls.CallTime) == month)
            .group_by(BVSCalls.CallFrom)
            .order_by(func.SUM(BVSCalls.Cost).desc())  # Sort by highest cost
            .all()
        )

        # Format data for rendering
        details = [
            {"extension": row.extension, 
             "call_count": row.call_count, 
             "total_cost": row.total_cost or 0}
            for row in extension_data
        ]

        return render_template("details.html", year=year, month=month, details=details)

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Something went wrong", "details": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
