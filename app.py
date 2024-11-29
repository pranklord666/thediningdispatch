from flask import Flask, request, jsonify, send_from_directory
import csv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('.', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css', mimetype='text/css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js', mimetype='application/javascript')

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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
