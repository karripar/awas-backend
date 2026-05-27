from flask import Blueprint, request, jsonify
from database import get_db, close_db
from utils import generate_id

feed_bp = Blueprint('feed', __name__, url_prefix='/api')

@feed_bp.route('/feed', methods=['GET'])
def get_feed():
    """Get feed posts - supports search"""
    search = request.args.get('search', '').strip()
    user_id = request.headers.get('X-User-ID', '').strip()
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        # VULNERABILITY: SQL Injection - search parameter is not sanitized
        if search:
            # This is vulnerable to SQL injection
            query = f"""
                SELECT p.*, u.username FROM posts p
                JOIN users u ON p.user_id = u.user_id
                WHERE (p.private = 0 OR p.user_id = '{user_id}')
                AND p.title LIKE '%{search}%'
                ORDER BY p.created_at DESC
            """
            cursor.execute(query)
        else:
            # Get public posts and user's private posts
            query = """
                SELECT p.*, u.username FROM posts p
                JOIN users u ON p.user_id = u.user_id
                WHERE p.private = 0 OR p.user_id = ?
                ORDER BY p.created_at DESC
            """
            cursor.execute(query, [user_id])
        
        posts = cursor.fetchall()
        close_db(db)
        
        result = [dict(post) for post in posts]
        return jsonify({'posts': result}), 200
    
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500

@feed_bp.route('/feed', methods=['POST'])
def create_post():
    """Create a new post"""
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title', '').strip()
    text = data.get('text', '').strip()
    private = data.get('private', False)
    
    if not user_id or not title or not text:
        return jsonify({'error': 'Missing fields'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    try:
        post_id = generate_id()
        cursor.execute('''
            INSERT INTO posts (post_id, user_id, title, text, private)
            VALUES (?, ?, ?, ?, ?)
        ''', (post_id, user_id, title, text, int(private)))
        
        db.commit()
        close_db(db)
        
        return jsonify({
            'message': 'Post created successfully',
            'post_id': post_id
        }), 201
    
    except Exception as e:
        close_db(db)
        return jsonify({'error': str(e)}), 500
