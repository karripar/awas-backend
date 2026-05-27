from flask import Blueprint, request, jsonify
import sqlite3
from database import get_db, close_db
from utils import simple_hash, generate_id

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing fields'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        user_id = generate_id()
        hashed_password = simple_hash(password)
        
        cursor.execute('''
            INSERT INTO users (user_id, username, email, password, role)
            VALUES (?, ?, ?, ?, 'user')
        ''', (user_id, username, email, hashed_password))
        
        db.commit()
        close_db(db)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'username': username
        }), 201
    
    except sqlite3.IntegrityError:
        close_db(db)
        return jsonify({'error': 'Registration failed'}), 409
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY: SQL injection. This intentionally combines user input
    # directly into the login query for the AWAS project demo.
    try:
        hashed_password = simple_hash(password)
        query = (
            f"SELECT * FROM users "
            f"WHERE username = '{username}' "
            f"AND password = '{hashed_password}'"
        )
        cursor.execute(query)
        user = cursor.fetchone()
        
        if not user:
            close_db(db)
            return jsonify({'error': 'Invalid username or password'}), 401
        
        close_db(db)
        
        # Create a simple session token
        # VULNERABILITY: Weak token - just user_id, TODOO: make it a bit more complex 
        session_token = user['user_id']
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
            'session_token': session_token
        }), 200
    
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    # VULNERABILITY: No real session management
    # TODOO: add better vulnerability here
    return jsonify({'message': 'Logged out successfully'}), 200
