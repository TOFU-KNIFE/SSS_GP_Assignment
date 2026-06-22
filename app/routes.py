from flask import Blueprint, request, jsonify
from app import db
from app.models import User
import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import re

auth = Blueprint('auth', __name__)

# Input validation helper
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

# Register route
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Input validation
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'All fields are required'}), 400

    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400

    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Hash password with bcrypt
    password_hash = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Create new user
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=password_hash.decode('utf-8'),
        role='user'
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


# Login route
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    # Find user
    user = User.query.filter_by(username=data['username']).first()

    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is disabled'}), 403

    # Generate JWT token
    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=1)
    )

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'role': user.role
    }), 200


# Protected route example
@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': str(user.created_at)
    }), 200


# Logout route
@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logged out successfully'}), 200