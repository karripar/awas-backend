import os

from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.auth import auth_bp
from routes.feed import feed_bp
from routes.admin import admin_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)

    session_cookie_secure = os.environ.get("SESSION_COOKIE_SECURE", "false").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    session_cookie_samesite = os.environ.get("SESSION_COOKIE_SAMESITE")
    if not session_cookie_samesite:
        session_cookie_samesite = "None" if session_cookie_secure else "Lax"

    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "change-me-in-production"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=session_cookie_secure,
        SESSION_COOKIE_SAMESITE=session_cookie_samesite,
        SESSION_COOKIE_NAME=os.environ.get("SESSION_COOKIE_NAME", "awas_session"),
    )

    frontend_origin = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")

    CORS(app, supports_credentials=True, origins=[frontend_origin])
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(admin_bp)
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        from flask import jsonify
        return jsonify({'status': 'ok'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='localhost', port=5000)
