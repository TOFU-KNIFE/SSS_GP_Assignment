from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    # Get current user
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Check if admin
    if not current_user or current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403

    # Return all users
    users = User.query.all()
    return jsonify({
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'is_active': user.is_active,
                'created_at': str(user.created_at)
            }
            for user in users
        ]
    }), 200