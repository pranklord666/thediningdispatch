from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

db.create_all()

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

    new_email = Email(email=email)
    db.session.add(new_email)
    db.session.commit()
    return jsonify({'message': 'Email received'})

@app.route('/download-emails')
def download_emails():
    emails = Email.query.all()
    if not emails:
        return "No emails found.", 404

    import csv
    from io import StringIO
    from flask import make_response

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['email'])
    for email in emails:
        writer.writerow([email.email])

    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=emails.csv"
    response.headers["Content-type"] = "text/csv"
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
