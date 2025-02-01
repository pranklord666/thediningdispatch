from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

# Define the Flask app
app = Flask(__name__)
CORS(app, origins=["https://thediningdispatch.com"])

# Helper function to connect to the database
def query_database(query, params=()):
    try:
        db_path = 'dining_dispatch.db'

        # Log the database path and its existence
        print(f"Checking database file: {db_path}")
        if not os.path.exists(db_path):
            print("Database file not found!")
            return []

        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like row access
        cursor = conn.cursor()

        # Log the query and parameters
        print("Executing query:", query)
        print("With parameters:", params)

        # Execute and fetch results
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()

        # Log the results
        print(f"Query returned {len(results)} results.")
        return [dict(row) for row in results]

    except Exception as e:
        # Log any database errors
        print("Error in query_database:", str(e))
        return []

# Exact search endpoint
@app.route('/search', methods=['GET'])
def search():
    try:
        # Log the incoming request
        print("Incoming request to /search")
        print("Request args:", request.args)

        # Extract query parameters
        style = request.args.get('Style', '').strip()
        cuisine = request.args.get('Cuisine', '').strip()
        location = request.args.get('Location', '').strip()

        # Log the extracted parameters
        print(f"Search parameters: Style={style}, Cuisine={cuisine}, Location={location}")

        # Construct the search query
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

        # Execute the query
        print("Constructed query:", query)
        print("Parameters:", params)
        results = query_database(query, params)

        # Check and return results
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
        # Log the error
        print("Error in /search route:", str(e))
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

# Main entry point
if __name__ == '__main__':
    # Log the working directory and database file
    print("Starting application...")
    print("Working directory:", os.getcwd())
    print("Database exists:", os.path.exists('dining_dispatch.db'))

    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))  # Render provides the PORT environment variable
    app.run(host='0.0.0.0', port=port, debug=True)
