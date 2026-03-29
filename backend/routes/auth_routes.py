from flask import Blueprint, request, jsonify
from models.models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    
    # Create new user
    user = User(
        email=data['email'],
        name=data['name'],
        user_type=data['user_type']  # 'recruiter' or 'jobseeker'
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'user_type': user.user_type
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'user_type': user.user_type
        }
    }), 200