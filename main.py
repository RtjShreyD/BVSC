from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

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

if __name__ == '__main__':
    app.run(debug=True)
