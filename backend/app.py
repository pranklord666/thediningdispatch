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

# Relax criteria function
def relax_criteria(food_type, location, subway_station, mood):
    try:
        # Order of relaxing criteria: mood, subway_station, food_type, location
        criteria = [
            {"query": " AND mood LIKE ?", "param": mood},
            {"query": " AND subway_station LIKE ?", "param": subway_station},
            {"query": " AND food_type LIKE ?", "param": food_type},
            {"query": " AND location LIKE ?", "param": location},
        ]

        for i in range(len(criteria)):
            query = "SELECT * FROM restaurants WHERE 1=1"
            params = []

            # Include only the first `len(criteria) - i` criteria
            for j in range(len(criteria) - i):
                if criteria[j]["param"]:
                    query += criteria[j]["query"]
                    params.append(f"%{criteria[j]['param']}%")

            # Execute the query
            print(f"Relaxed query attempt {i + 1}: {query} with params {params}")
            results = query_database(query, params)
            if results:
                return results

        return []  # Return empty if no results are found even after relaxing
    except Exception as e:
        print("Error in relax_criteria:", str(e))
        return []

# Exact search endpoint
@app.route('/search', methods=['GET'])
def search():
    try:
        # Log the incoming request
        print("Incoming request to /search")
        print("Request args:", request.args)

        # Extract query parameters
        food_type = request.args.get('food_type', '').strip()
        location = request.args.get('location', '').strip()
        subway_station = request.args.get('subway_station', '').strip()
        mood = request.args.get('mood', '').strip()

        # Log the extracted parameters
        print(f"Search parameters: food_type={food_type}, location={location}, subway_station={subway_station}, mood={mood}")

        # Full search query
        query = "SELECT * FROM restaurants WHERE 1=1"
        params = []

        if food_type:
            query += " AND food_type LIKE ?"
            params.append(f"%{food_type}%")
        if location:
            query += " AND location LIKE ?"
            params.append(f"%{location}%")
        if subway_station:
            query += " AND subway_station LIKE ?"
            params.append(f"%{subway_station}%")
        if mood:
            query += " AND mood LIKE ?"
            params.append(f"%{mood}%")

        # Execute the query
        print("Constructed query:", query)
        print("Parameters:", params)
        results = query_database(query, params)

        # If no results, progressively relax the criteria
        if not results:
            print("No exact results found. Trying relaxed criteria...")
            relaxed_results = relax_criteria(food_type, location, subway_station, mood)
            if relaxed_results:
                return jsonify({
                    "message": "Nothing matches your exact search, but here's something close:",
                    "data": relaxed_results
                })
            else:
                print("No results found even with relaxed criteria.")
                return jsonify({
                    "message": "No restaurants match your search criteria.",
                    "data": []
                })

        # Return exact match results
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
