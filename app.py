from flask import Flask, request, jsonify
import csv

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    with open('emails.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email])
    return jsonify({'message': 'Email received'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
