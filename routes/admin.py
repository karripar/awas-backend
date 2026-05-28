from flask import Blueprint, request, jsonify
from database import get_db, close_db

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/feed/delete', methods=['DELETE'])
def delete_post():
    """Delete a post - admins or post owners only"""
    data = request.get_json(silent=True) or {}
    post_id = data.get('post_id')
    current_user_id = data.get('current_user_id') or data.get('user_id') or request.headers.get('X-User-ID', '').strip()

    if not post_id or not current_user_id:
        return jsonify({'error': 'Missing fields'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('SELECT user_id, role FROM users WHERE user_id = ?', (current_user_id,))
        current_user = cursor.fetchone()
        if not current_user:
            return jsonify({'error': 'Unauthorized'}), 403

        cursor.execute('SELECT user_id FROM posts WHERE post_id = ?', (post_id,))
        post = cursor.fetchone()
        if not post:
            return jsonify({'error': 'Post not found'}), 404

        if current_user['role'] != 'admin' and post['user_id'] != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        cursor.execute('DELETE FROM posts WHERE post_id = ?', (post_id,))
        db.commit()
        
        return jsonify({'message': 'Post deleted successfully'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        close_db(db)


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


