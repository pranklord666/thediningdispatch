from flask import Flask, request, jsonify, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os
import csv
from io import StringIO

app = Flask(__name__)

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Adjust for SQLAlchemy 1.4 and above
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    # Fallback to local SQLite database for development
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    if not email:
        return jsonify({'message': 'Email is required'}), 400

    new_email = Email(email=email)
    try:
        db.session.add(new_email)
        db.session.commit()
        return jsonify({'message': 'Email received'})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred'}), 500

@app.route('/download-emails')
def download_emails():
    emails = Email.query.all()
    if not emails:
        return "No emails found.", 404

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

@app.route('/list-emails')
def list_emails():
    emails = Email.query.all()
    email_list = [email.email for email in emails]
    return jsonify({'emails': email_list})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
