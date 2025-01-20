from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Define the Flask app
app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for testing; restrict in production.

# Helper function to connect to the database
def query_database(query, params=()):
    try:
        db_path = 'dining_dispatch.db'

        # Ensure the database exists
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}.")
            return []

        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Log the query and parameters
        print("Executing query:", query)
        print("With parameters:", params)

        # Execute the query
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # Log the results
        print(f"Query returned {len(results)} results.")
        return [dict(row) for row in results]

    except Exception as e:
        print(f"Database query error: {e}")
        return []

# Search endpoint
@app.route('/search', methods=['GET'])
def search():
    try:
        # Extract query parameters
        food_type = request.args.get('food_type', '').strip()
        location = request.args.get('location', '').strip()
        price = request.args.get('price', '').strip()

        # Build the query dynamically
        query = "SELECT * FROM restaurants WHERE 1=1"
        params = []

        if food_type:
            query += " AND type_of_food LIKE ?"
            params.append(f"%{food_type}%")
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")
        if price:
            query += " AND price = ?"
            params.append(price)

        # Log the constructed query
        print("Constructed query:", query)
        print("Query parameters:", params)

        # Execute the query
        results = query_database(query, params)

        # Return the results
        if not results:
            return jsonify({
                "message": "No restaurants match your search criteria.",
                "data": []
            })

        return jsonify({
            "message": "Here are the results for your search:",
            "data": results
        })

    except Exception as e:
        print(f"Error in /search route: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

# Main entry point
if __name__ == '__main__':
    # Check if the database exists
    print("Starting application...")
    print(f"Database exists: {os.path.exists('dining_dispatch.db')}")

    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
