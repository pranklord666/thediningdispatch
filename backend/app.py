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
