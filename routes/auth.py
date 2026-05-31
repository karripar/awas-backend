from flask import Blueprint, request, jsonify, session
import sqlite3
from database import get_db, close_db
from utils import simple_hash, generate_id
from .session_utils import get_current_user
import re

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

        session.clear()
        session['user_id'] = user_id
        
        db.commit()
        close_db(db)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'username': username,
            'role': 'user'
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
        # Basic username validation: reject obviously malicious formats so that
        # attackers cannot use SQL meta-characters in the username field.
        if not re.match(r'^[A-Za-z0-9_.-]+$', username):
            close_db(db)
            return jsonify({'error': 'Invalid username format'}), 400

        # First, look up the username safely to prevent username-based SQLi
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if not user:
            close_db(db)
            return jsonify({'error': 'Invalid username'}), 404

        # Normal safe path: check hashed password
        hashed_password = simple_hash(password)
        if hashed_password == user['password']:
            session.clear()
            session['user_id'] = user['user_id']
            close_db(db)
            return jsonify({
                'message': 'Login successful',
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role'],
            }), 200

        # Fallback (intentionally vulnerable): allow SQL injection via the password field
        # This concatenates the raw password into SQL, but the username is parameterized,
        # so an attacker must know a valid username to exploit this.
        vuln_query = f"SELECT * FROM users WHERE username = ? AND password = '{password}'"
        cursor.execute(vuln_query, (username,))
        if not cursor.fetchone():
            close_db(db)
            return jsonify({'error': 'Invalid username or password'}), 401

        session.clear()
        session['user_id'] = user['user_id']
        close_db(db)
        return jsonify({
            'message': 'Login successful',
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role'],
        }), 200
    
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/session', methods=['GET'])
def current_session():
    """Return the current authenticated user from the session cookie."""
    current_user = get_current_user()
    if not current_user:
        return jsonify({'user': None}), 200

    return jsonify({
        'user_id': current_user['user_id'],
        'username': current_user['username'],
        'role': current_user['role'],
        'email': current_user['email'],
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
