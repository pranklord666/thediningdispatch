from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Helper function to connect to the database
def query_database(query, params=()):
    conn = sqlite3.connect('dining_dispatch.db')
    conn.row_factory = sqlite3.Row  # Enable dict-like row access
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

# Relax criteria function
def relax_criteria(food_type, location, subway_station, mood):
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
        results = query_database(query, params)
        if results:
            return results

    return []  # Return empty if no results are found even after relaxing

# Exact search endpoint
@app.route('/search', methods=['GET'])
def search():
    food_type = request.args.get('food_type', '').strip()
    location = request.args.get('location', '').strip()
    subway_station = request.args.get('subway_station', '').strip()
    mood = request.args.get('mood', '').strip()

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
    results = query_database(query, params)

    # If no results, progressively relax the criteria
    if not results:
        relaxed_results = relax_criteria(food_type, location, subway_station, mood)
        if relaxed_results:
            return jsonify({
                "message": "Nothing matches your exact search, but here's something close:",
                "data": relaxed_results
            })
        else:
            return jsonify({
                "message": "No restaurants match your search criteria.",
                "data": []
            })
    return jsonify({
        "message": "Here are the results for your search:",
        "data": results
    })

if __name__ == '__main__':
    app.run(debug=True)
