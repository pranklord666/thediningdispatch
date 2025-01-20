from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def query_database(query, params=()):
    db_path = 'dining_dispatch.db'
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Database error: {e}")
        return []

@app.route('/search', methods=['GET'])
def search():
    food_type = request.args.get('food_type', '').strip()
    location = request.args.get('location', '').strip()
    price = request.args.get('price', '').strip()

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

    results = query_database(query, params)
    if not results:
        return jsonify({"message": "No results found.", "data": []})

    for restaurant in results:
        restaurant['instagram_iframe'] = f"<iframe src='{restaurant['instagram_link']}/embed' width='400'></iframe>" if restaurant['instagram_link'] else None
        restaurant['chef_link'] = f"<a href='{restaurant['chef']}' target='_blank'>{restaurant['chef'].split('/')[-1]}</a>" if 'http' in restaurant['chef'] else restaurant['chef']

    return jsonify({"message": "Results found.", "data": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
