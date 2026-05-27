from flask import Blueprint, request, jsonify
from database import get_db, close_db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/feed/delete', methods=['DELETE'])
def delete_post():
    """Delete a post - ADMIN ONLY"""
    data = request.get_json()
    post_id = data.get('post_id')
    user_id = data.get('user_id')
    
    if not post_id or not user_id:
        return jsonify({'error': 'Missing fields'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        # VULNERABILITY: No proper authorization check - relies on frontend validation
        # Any user who knows a post_id and provides user_id can delete
        cursor.execute('DELETE FROM posts WHERE post_id = ?', (post_id,))
        db.commit()
        close_db(db)
        
        return jsonify({'message': 'Post deleted successfully'}), 200
    
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/users', methods=['GET'])
def list_users():
    """List users (ADMIN view)"""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT user_id, username, email, role, created_at FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        close_db(db)
        users = [dict(r) for r in rows]
        return jsonify({'users': users}), 200
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/user/delete', methods=['DELETE'])
def delete_user():
    """Delete a user - ADMIN ONLY"""
    data = request.get_json()
    user_id_to_delete = data.get('user_id')
    current_user_id = data.get('current_user_id')
    
    if not user_id_to_delete or not current_user_id:
        return jsonify({'error': 'Missing fields'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        # VULNERABILITY: No role verification - relies on frontend validation only
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id_to_delete,))
        db.commit()
        close_db(db)
        
        return jsonify({'message': 'User deleted successfully'}), 200
    
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500


