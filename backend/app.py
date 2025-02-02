from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Define the Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure CORS headers are always included
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# Helper function to connect to the database
def query_database(query, params=()):
    try:
        db_path = os.path.join(os.path.dirname(__file__), 'dining_dispatch.db')

        print(f"Checking database file: {db_path}")
        if not os.path.exists(db_path):
            print("Database file not found!")
            return []

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like row access
        cursor = conn.cursor()

        print("Executing query:", query)
        print("With parameters:", params)

        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        print(f"Query returned {len(results)} results.")
        return [dict(row) for row in results]

    except Exception as e:
        print("Error in query_database:", str(e))
        return []

# Exact search endpoint
@app.route('/search', methods=['GET'])
def search():
    try:
        print("Incoming request to /search")
        print("Request args:", request.args)

        style = request.args.get('Style', '').strip()
        cuisine = request.args.get('Cuisine', '').strip()
        location = request.args.get('Location', '').strip()

        print(f"Search parameters: Style={style}, Cuisine={cuisine}, Location={location}")

        query = "SELECT * FROM restaurants WHERE 1=1"
        params = []

        if style:
            query += " AND Style LIKE ?"
            params.append(f"%{style}%")
        if cuisine:
            query += " AND Cuisine LIKE ?"
            params.append(f"%{cuisine}%")
        if location:
            query += " AND Location = ?"
            params.append(location)

        print("Constructed query:", query)
        print("Parameters:", params)
        results = query_database(query, params)

        if not results:
            return jsonify({
                "message": "No restaurants match your search criteria.",
                "data": []
            })

        print(f"Found {len(results)} exact results.")
        return jsonify({
            "message": "Here are the results for your search:",
            "data": results
        })

    except Exception as e:
        print("Error in /search route:", str(e))
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

# Main entry point
if __name__ == '__main__':
    print("Starting application...")
    print("Working directory:", os.getcwd())
    print("Database exists:", os.path.exists('dining_dispatch.db'))

    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT environment variable
    app.run(host='0.0.0.0', port=port, debug=True)
