from flask import Flask, request, jsonify, send_from_directory, send_file
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
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    if not os.path.exists('emails.csv'):
        with open('emails.csv', 'w') as file:
            file.write('email\n')
    with open('emails.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([email])
    return jsonify({'message': 'Email received'})

@app.route('/download-emails')
def download_emails():
    try:
        return send_file('emails.csv', as_attachment=True)
    except FileNotFoundError:
        return "Le fichier emails.csv n'existe pas.", 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
