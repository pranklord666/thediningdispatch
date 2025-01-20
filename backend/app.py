from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Helper function to query the database
def query_database(query, params=()):
    try:
        db_path = 'dining_dispatch.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Database query error: {e}")
        return []

@app.route('/restaurant/<name>.json', methods=['GET'])
def restaurant_json(name):
    try:
        query = """
        SELECT 
            name, address, subway, comments, mood, 
            instagram_link, booking, menu, chef
        FROM restaurants
        WHERE name = ?
        """
        result = query_database(query, (name,))
        if not result:
            return jsonify({"message": "Restaurant not found"}), 404

        restaurant = result[0]
        instagram_iframe = f"<iframe src='{restaurant['instagram_link']}/embed' width='400'></iframe>" if restaurant['instagram_link'] else None
        chef_link = f"<a href='{restaurant['chef']}' target='_blank'>{restaurant['chef'].split('/')[-1]}</a>" if 'http' in restaurant['chef'] else restaurant['chef']

        response = {
            "name": restaurant["name"],
            "address": restaurant["address"],
            "subway": restaurant["subway"],
            "comments": restaurant["comments"],
            "mood": restaurant["mood"],
            "instagram_iframe": instagram_iframe,
            "booking_link": restaurant["booking"],
            "menu_link": restaurant["menu"],
            "chef_link": chef_link,
        }

        return jsonify(response)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
