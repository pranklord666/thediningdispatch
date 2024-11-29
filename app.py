from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    if not os.path.exists('emails.csv'):
        with open('emails.csv', 'w') as file:
            file.write('email\n')
    with open('emails.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email])
    return jsonify({'message': 'Email received'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
