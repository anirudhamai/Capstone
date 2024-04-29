# backend.py

from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_migrate import Migrate
import jwt  # Add jwt library for token generation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '7de5106d15bc506be7b57649309e7c38'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)

# Define HomeownerPhoto model   
class HomeownerPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    homeowner_name = db.Column(db.String(100), nullable=False)
    image_path = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone_number')
    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists'}), 403
    new_user = User(username=username, password=generate_password_hash(password),phone_number=phone)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Route for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    # Generate JWT token upon successful login
    token = jwt.encode({'user_id': user.id}, app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token}), 200

# Route for user logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

# Route for uploading homeowner photos
@app.route('/upload', methods=['POST'])
def upload_photo():
    # Add authentication logic here
    data = request.form
    homeowner_name = data.get('homeowner_name')
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    # Add logic for file validation and saving
    filename = f"{homeowner_name}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.jpg"
    # Save file logic here
    new_photo = HomeownerPhoto(homeowner_name=homeowner_name, image_path=filename)
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({'message': 'Photo uploaded successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
